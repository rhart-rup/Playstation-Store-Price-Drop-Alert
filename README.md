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

* Track the price of any game on the UK Playtsation Store 
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

## Requirements & Setup

In order to run the script successfully you must: 

* Create a virtual environment from the *requirements.txt* file in this repo
* Create Gmail API credentials as follows:  
  1. Complete steps 1. and 2. [here](https://developers.google.com/gmail/api/quickstart/python). In Step 2. you should change the SCOPES variable value in quickstart.py to "www.gmail.com" to give you access to send emails from your gmail account using the API. 
  2. Ensure you have successfully created a *token.pickle* file
* Create an initial *game_prices.csv* by editing the template *game_prices.csv* file in this repo. You simply need to fill in a game name and game_id to add each game you wish to track (see above for details on getting the game_id).
* Place the *main.py*, *game_prices.csv* and *token.pickle* files in the same directory.
* Run the main.py file using the virtual environment.


- Playstation url to get game_id - grabbing the game ID from the playstation store updating a line in the csv...
- adding and removing games (delete row..add row...)
 
## Automation

set for daily runs, I used plists and converted to an executable file on mac. If day is missed it will still work. 
