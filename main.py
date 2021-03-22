import requests
from bs4 import BeautifulSoup
import time
import plotly
import numpy as np
import pandas as pd
import datetime as dt
import cufflinks as cf

import subprocess
import traceback
from sys import exit
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import pickle
import os.path
from googleapiclient.discovery import build

# Set working directory to the project folder
os.chdir("<replace_with_path_to_project_folder>")

def extract_price(game_page):
    """Finds and returns the price of a game on a playstation store
    web page. If no price is found, returns null.
    """
    soup = BeautifulSoup(game_page.text, features="html.parser")
    price = soup.find('span', class_='psw-h3')
    if price is None:
        return np.nan
    else:
        # Remove '£' from price and return the value
        return float(price.get_text().replace('£', ''))

def get_latest_non_null(row):
    """Returns the most recent, non-null price of a row.
    Returns -1 if all prices in row are null.
    """
    # Value returned if no non-null value exists
    price = -1
    # Loops through the row backwards and returns first non-null value
    for element in reversed(row):
        # Check element is not null (null values dont equal themselves)
        if element == element:
            price = element
            break
    return price

def create_message(sender, to, subject, price_drop, failures, nans):
    """Create, Encode and return Gmail email.

    Checks if there are rows for the price_drop, failures and nans
    dataframes. If a dataframe has rows, it is included as a table
    in the html body of them email.
    """
    message = MIMEMultipart()
    # html contains the HTML code for the email body
    html = """<html>
      <head></head>
      <body>"""
    # If price_drop df has rows, its table is included in the email
    if price_drop.shape[0] > 0:
        html += '<p><b>Price Drops:</b></p>'
        html += price_drop.to_html(escape=False, index = False, justify = 'center')
    # If failures df has rows, its table is included in the email
    if len(failures) > 0:
        html += '<br><p><b>Failed to Scrape:</b></p>'
        html += '<br>'.join(failures)
    # If nans df has rows, its table is included in the email
    if nans.shape[0] > 0:
        html += '<br><p><b>Price Not Found:</b></p>'
        html += nans.to_html()
    html += """<br></body>
        </html>"""

    part1 = MIMEText(html, 'html')
    message.attach(part1)

    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    # Message encoded as required for the Gmail API
    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {'raw': raw_message.decode("utf-8")}

# Wait 10 seconds in case computer was asleep (give time for
# an internet connection to be established)
time.sleep(10)

# Attempt to retrieve google.com to confirm internet connection,
# wait 5 minutes and try again if there is a error (no connection).
# If an error occurs the second time, a Pop-up error message is
# displayed and script is terminated.
try:
    requests.get('https://www.google.com/')
except:
    time_of_error = time.time()
    while time.time() - time_of_error < 300:
        time.sleep(1)
    try:
        requests.get('https://www.google.com/')
    except:
        # Create Mac OS popup error message
        applescript = """
        display dialog "Playstation_scraper could not connect to the internet." ¬
        with title "Internet Connection Error" ¬
        with icon caution ¬
        buttons {"OK"}
        """
        subprocess.call("osascript -e '{}'".format(applescript), shell=True)
        exit('exit')

# The game price data is stored in Game_prices.csv. Each row
# corresponds to a different game, each column is the price of a game
# on a certain day with the days ordered sequentially from left to
# right. The header for each column is the date the price was taken.
# The first column stores the name of the game which is used
# as an index. The second column stores the game ID used by the
# playstation store.
df = pd.read_csv('game_prices.csv', ',', index_col='game')

# Convert the date column headers to date-time format
category_headers = df.columns[:1].tolist()
date_headers = df.columns[1:]
converted_date_headers = pd.to_datetime(date_headers, format='%d/%m/%Y').date.tolist()
df.columns = category_headers + converted_date_headers

# The full url for a game is the base url with the game ID added at
# the end.
base_url = 'https://store.playstation.com/en-gb/product/'

# time_delay is the seconds waited between subsequent GET requests
time_delay = 10
# game_price records the price of each game today
game_price = []
time_last_request = time.time()
# failures records the game url's which result in an error when requested.
failures = []
# The game_id column of df defines the game_id for each game.
# The code loops through this and for each game id it makes a
# get request and scrapes the price of that game from its webpage.
for game_id in df.game_id:
    # Waits between subsequent GET requests.
    while time.time() - time_last_request < time_delay:
        time.sleep(1)

    try:
        # full game url is base_url + game id
        game_page = requests.get(base_url + game_id)
        time_last_request = time.time()
        game_price.append(extract_price(game_page))
    # If GET request or price extraction failed, wait 300 seconds
    # and try again
    except:
        time_error = time.time()
        while time.time() - time_error < 300:
            time.sleep(1)
        try:
            game_page = requests.get(base_url + game_id)
            time_last_request = time.time()
            game_price.append(extract_price(game_page))
        except:
            # both GET requests failed so record as failure
            failures.append(base_url + game_id)
            # Record game price today as null
            game_price.append(np.nan)

# Add todays game prices as new column in df
date = dt.date.today()
df[date] = game_price

# Below generates a separate plot of price over time for each game in df.
n_rows = df.shape[0]
# plotly layout used to define the layout of the plot.
layout1 = cf.Layout(xaxis=dict(autorange=True, dtick='M1'),
                    yaxis=dict(title=dict(standoff=0, text='')),
                    height=150 * n_rows,
                    width=1200,
                    margin=dict(pad=0, t=100, l=0.9, r=0.9, b=1),
                    showlegend=False,
                    title=dict(text='Price of Games on Playstation Store',
                               x=0.5, y=0.99, xanchor='center')
                )
# df is transposed so each column is a game, with the price on
# each dates in the rows. The game_id column in excluded
# by .iloc[1:,]
plotting_df = df.T.iloc[1:, ]
# Sub-plots will be in 2 columns, this is defined by the shape
# paramater, which takes a tuple (rows, columns). To calculate
# the rows we divide the number of games (total rows in df) by 1.9 and
# round the answer. e.g. if there are 7 games, we divide by 1.9 and
# round up giving us 4 rows. We use 1.9 because if we divide by 2 Python
# sometimes rounds numbers ending in 0.5 down rather than up.
shape1 = (round(n_rows / 1.9), 2)
# Plot price variation over time for each game
fig = plotting_df.iplot(subplots=True, shape=shape1,
                        subplot_titles=True, vertical_spacing=0.08,
                        horizontal_spacing=0.1, layout=layout1,
                        asFigure=True, color='orange', width=2)
fig.update_layout(hovermode='x unified')

# Fixes the opacity of the lines so all lines are fully visible
# (by default cufflinks gave variable opacity to the lines).
for i in fig['data']:
    i['line']['color'] = "rgba(255, 153, 51, 1.0)"
# Sets color and style of the subplot titles
for i in fig['layout']['annotations']:
    i['font'] = dict(size=14, color='orange')
# Adds date selector buttons (e.g. 'last month') to plots
fig.update_xaxes(
    rangeselector = dict(
        yanchor='bottom',
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
                       ])
    )
)
# Set y axis range
fig.update_yaxes(nticks=8, rangemode='tozero', range=[0,60])
fig.write_html("Game Prices.html")

# The next section identifies price drops and prices that couldn't
# be found (nan_prices)
price_drops = []
nan_prices = []

# Excludes dataframes with data from only 1 date and only runs if the latest
# data is from today
if (df.shape[1] > 2):
    # We want to find the latest price before todays data so
    # we exclude todays column and the game_id column
    # This is to account for any NAN values in the data.
    df_prices_before_today = df.iloc[:, 1:-1]
    # Most recent non-null price for each game is found. Note that if
    # no non-null old price exists, the most recent price will be -1
    most_recent_price = [get_latest_non_null(row)
                         for row in df_prices_before_today.to_numpy()]
    # Loops through the games and identifies any price drops
    for game, game_id, new_price, old_price in zip(df.index, df.game_id,
                                                   game_price, most_recent_price):

        # Price drops only calculated if there is a valid price for
        # today (the value is not null) and a valid last price to
        # compare it to (most_recent_price is not -1)
        if (new_price == new_price) & (old_price > 0):
            price_delta = old_price - new_price
            # Only notify price drops larger than £0.5
            if price_delta > 0.5:
                html_link = '<a href="' + base_url \
                            + game_id + '"><div style="height:100%;width:100%">' \
                            + game + '</div></a>'
                price_drops.append([html_link, old_price, new_price, price_delta])
        # Also tracks any prices today that have returned a nan value
        elif new_price != new_price:
            nan_prices.append([game, base_url + game_id])
    # Replace nan prices today in df with the latest non-null value
    # (assume price has stayed the same if no price was found today)
    for price_today, game, most_recent_price in zip(game_price,
                                                    df.index.values.tolist(),
                                                    most_recent_price):
        if (price_today != price_today) & (most_recent_price >0):
            df.loc[game,date] = most_recent_price

drops = len(price_drops)
fails = len(failures)
nans = len(nan_prices)

# Checks if there is anything to email (will email price drops,
# request failures and nan prices).
if drops + fails + nans > 0:
    # Builds subject line for email including number of drops. failures
    # or null prices
    subject = 'Rupe Playstation Price Drop Alerts: '
    if drops > 0:
        subject += str(drops) + ' Drops, '
    if fails > 0:
        subject += str(fails) + ' Failures, '
    if nans > 0:
        subject += str(nans) + ' Price Not Found'
    # Create dataframe of price drop info to be emailed as a table
    price_drop_df = pd.DataFrame(price_drops,
                                 columns=['Game', 'Old Price',
                                          'New Price', 'Price Drop']
                            )
    price_drop_df = price_drop_df.sort_values(by=['Price Drop'],
                                              ascending = False)
    # Create dataframe of null prices (no price found) to be emailed
    # as a table
    nan_prices_df = pd.DataFrame(nan_prices, columns=['Game', 'Game_ID'])
    # Create email using Gmail API
    try:
        # Create email message
        mail = create_message('me', 'ruperthart92@gmail.com', subject,
                              price_drop_df, failures, nan_prices_df)
        # Check that a token.pickle exists containing the gmail
        # credentials and load them
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # Create the gmail service using credentials and send message
        service = build('gmail', 'v1', credentials=creds)
        message = (service.users().messages().send(userId='me', body=mail)
                   .execute())
        print('email sent')
    except:
        # Mac OS error alert in case gmail email fails to send
        applescript = """
        display dialog "Playstation_scraper email failed to send." ¬
        with title "Playstation_scraper: Email Failed" ¬
        with icon caution ¬
        buttons {"OK"}
        """
        subprocess.call("osascript -e '{}'".format(applescript), shell=True)
        print('email failed')
        traceback.print_exc()

# Convert date time headers to strings with the same format as the
# original csv (this is the format that excel uses when you save as csv)
dates = df.columns[1:].tolist()
dates_as_strings = [date_obj.strftime('%d/%m/%Y') for date_obj in dates]
df.columns = df.columns[:1].tolist() + dates_as_strings

df.to_csv('game_prices.csv')
print('ran on ', date)
