# Covid-Recovery-Dashboard-DVA

## Overview
We have built a "COVID recovery dashboard" to help businesses take decisions to recover from the pandemic and return to the new normalcy. We have used an innovative approach by combining various factors to predict and guide the public to make meaningful decisions.

## Dashboard

Dashboard link: https://covid-recovery-dashboard.herokuapp.com/

The dashboard has two sections:

1. Key Performance Indicators




2. Prediction Engine



## Installation

### Software for the dashboard

### Code
Python version 3.8.0
Libraries to install: pandas, numpy, sklearn, statsmodels, datetime, inspect, dash


## Data Collection
All dataset are directly called within the python script except the following:
### Covid19 Cases:
Download https://covid.ourworldindata.org/data/owid-covid-data.csv as owid-covid-data.csv
### Temeperature: 
Register an account at https://data.world/data-society/global-climate-change-data. Download "GlobalLandTemperaturesByCountry.csv".
### Tweets:
Register an account and download all csvs at https://ieee-dataport.org/open-access/coronavirus-covid-19-tweets-dataset
### Flights:




The above dataset are downloaded and placed into the dataset folder.

## Execution 

#### Bringing up the dashboard is a simple two-step process:
1. Install all the required packages:
`pip install -r requirements.txt`
2. Execute the dash app
`python app.py`

