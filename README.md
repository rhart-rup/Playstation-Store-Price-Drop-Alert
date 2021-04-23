# Playstation Store Price Drop Alert
![price drop graphic](https://github.com/rhart-rup/Playstation-Store-Price-Drop-Alert/blob/main/Graphics/Graph3.png?raw=true)

## Overview

This project provides a python script that: 
* Scrapes the price for a set of games from the UK Playtsation Store
* Stores these historical prices in a csv file
* Provides an interactive dashboard of prices over time for the various games  
* Sends an email alert when a price drops

The script is intended to be run automatically once per day. See below for details on how this can be done on MacOS. 

## Features

### Track Any Game Any Time

You can track the prices of any game on the UK Playtsation Store simply by adding a new row to the game_prices.csv file. You can track as many games as you want and you can add and remove games at any time. 

### Interactive Historical Price Dashboard

Shows price history for each game in a separate chart. 

![](https://github.com/rhart-rup/Playstation-Store-Price-Drop-Alert/blob/main/Graphics/Example%20Dashboard.png)

### Price Drop Email Alerts

An email alert is sent containing all price drops for that day and includes html links to the Playstation Store pages for each game. 

![](https://github.com/rhart-rup/Playstation-Store-Price-Drop-Alert/blob/main/Graphics/Example%20email%20notification.png)  

### Error Notifications

Custom error messages are displayed if the script was unable to access the internet or if the email failed to send. 

![](https://github.com/rhart-rup/Playstation-Store-Price-Drop-Alert/blob/main/Graphics/Example%20Error%20Message.png)

Additionally, an email notifaction is sent if an error occured when scraping the price data.    

![](https://github.com/rhart-rup/Playstation-Store-Price-Drop-Alert/blob/main/Graphics/Failure%20Notification%20Email.png)

## Requirements & Setup

In order to run the script successfully you will need: 

run successfully before automating. 

- main.py plus requirements.txt
- token credentials from google (with link)
- Note Mac OS comments
- initial csv
- Playstation url to get game_id - grabbing the game ID from the playstation store updating a line in the csv...

 
## Automation

set for daily runs, I used plists and converted to an executable file on mac. If day is missed it will still work. 
