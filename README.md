# Playstation Store Price Drop Alert
![price drop graphic](https://github.com/rhart-rup/Playstation-Store-Price-Drop-Alert/blob/main/Graphics/Graph3.png?raw=true)

## Overview

This project provides a python script that: 
* Scrapes the price for a set of games from the UK Playtsation Store
* Stores these historical prices in a csv file
* Provides a dashboard of prices over time for the various games  
* Sends email alert when a price drops

The script is intended to be run automatically once per day. 

## Features

### Interactive Historical Price Dashboard

![](https://github.com/rhart-rup/Playstation-Store-Price-Drop-Alert/blob/main/Graphics/Example%20Dashboard.png)

### Price Drop Email Alerts

If there are one or more price drops, an email alert is sent containing all price drops for that day. The email includes html links to the Playstation Store page for each game whose price has dropped.

![](https://github.com/rhart-rup/Playstation-Store-Price-Drop-Alert/blob/main/Graphics/Example%20email%20notification.png)  

### Error Notifications

Custom error messages are displayed if the script was unable to access the internet or if the email failed to send. 

![](https://github.com/rhart-rup/Playstation-Store-Price-Drop-Alert/blob/main/Graphics/Example%20Error%20Message.png)

Additionally, an email notifaction is sent if an error occured when scraping the price data. The email will specifcy which games failed to scrape, provide an html link to the specific Playstation Store page and specify whether the scraping failed or returned a null value (or both).   

![](https://github.com/rhart-rup/Playstation-Store-Price-Drop-Alert/blob/main/Graphics/Failure%20Notification%20Email.png)


of hat monitors o pull the current price for  game from the UK Playstion Store

price drop alerts for number of games 
dashboard 
errors 
email alerts 

## Requirements & Setup
## Automation
