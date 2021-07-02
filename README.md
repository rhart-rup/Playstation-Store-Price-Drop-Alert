# Playstation Store Price Drop Alert
![price drop graphic](https://github.com/rhart-rup/Playstation-Store-Price-Drop-Alert/blob/main/Graphics/Graph3.png?raw=true)

## Overview

This project provides a python script that: 
* Scrapes the price for a set of games on the UK Playtsation Store
* Stores these historical prices in a csv file
* Provides an interactive dashboard of prices over time for the various games  
* Sends an email alert when a game price drops

The script is intended to be run automatically once per day and is robust to interruptions (i.e. still works if the script fails to run on some days). See below for details on how this automation can be done on MacOS. 

## Features

### Track Any Game Any Time

* Track the price of any game on the UK Playstation Store 
* Track as many games as you want
* Start and stop tracking games at any time. 

To track a game, you simply need the *game_id*. This can be found by navigating to the Playstation Store page for the game. The *game_id* is the text followng the last '/' of the url. 

![](https://github.com/rhart-rup/Playstation-Store-Price-Drop-Alert/blob/main/Graphics/game_ID%20example.png)

### Interactive Historical Price Dashboard

Shows price history for each game you are tracking in a separate chart. 

![](https://github.com/rhart-rup/Playstation-Store-Price-Drop-Alert/blob/main/Graphics/Example%20Dashboard.png)

### Price Drop Email Alert

An email alert is sent when a price drop is detected using the Gmail API. It includes links to the specific Playstation Store page for every game whose price dropped that day. 

![](https://github.com/rhart-rup/Playstation-Store-Price-Drop-Alert/blob/main/Graphics/Example%20email%20notification.png)  

### Error Notifications

Custom error messages are displayed if the script was unable to access the internet or if the email failed to send. 

![](https://github.com/rhart-rup/Playstation-Store-Price-Drop-Alert/blob/main/Graphics/Example%20Error%20Message.png)

Additionally, an email notifaction is sent if an error occured when scraping the price data. It contains links to the specific pages that failed to scrape.    

![](https://github.com/rhart-rup/Playstation-Store-Price-Drop-Alert/blob/main/Graphics/Failure%20Notification%20Email.png)

## Setup and Maintenance

### Initial Setup

In order to run the script you must: 

1. Create a virtual environment from the *requirements.txt* file in this repo.  
2. Create Gmail API credentials as follows:  
    1. Go [here](https://developers.google.com/gmail/api/quickstart/python) and complete steps 1. and 2. In Step 2. you must change the SCOPES variable in *quickstart.py* to "www.gmail.com". This permits the API to send emails from your Gmail account. 
    2. Confirm the above step created your *token.pickle* file.  
3. Create an initial *game_prices.csv* by editing the template *game_prices.csv* file in this repo. You simply need to fill in the game name (an arbitrary name that you choose to identify each game) and game_id to add each game you wish to track (see above for details on getting the game_id).
4. Place the *main.py*, *game_prices.csv* and *token.pickle* files in the same directory.
5. Run the main.py file using the virtual environment.

After the file is run, it will have generated the *Game Prices.html* file which is the interactive dashbaord. It will also have updated the *game_prices.csv* file with a new column. The column header is the date the script was run. The column records the price of each game in the file on that day. 

Each time the *main.py* script is run on subsequent days, a new column is added recording the latest prices for the games and the price dashboard is updated. When a price drop is detected, the email alert is sent. If the script is re-run on the same day, the latest price column is updated, it does not create another column. 

### Adding & Removing Games to Track

* To track a new game, add the game name and game_id on a new row in the *game_prices.csv*
* To stop tracking a game, delete the entire row of data for that game in the *game_prices.csv*, including the game name and game_id. Ensure there are no blank rows in the csv. 

## Automation On MacOS

set for daily runs, I used plists and converted to an executable file on mac. If day is missed it will still work. 
