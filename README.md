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
Python version 3.7
Libraries to install: pandas, numpy, sklearn, statsmodels, datetime, os, sys, inspect
Visit https://packaging.python.org/tutorials/installing-packages/ for python package installation


## Data Collection
All dataset are directly called within the python script except the following:
### Covid19 Cases:
Download https://covid.ourworldindata.org/data/owid-covid-data.csv as owid-covid-data.csv
### Temeperature: 
Register an account at https://data.world/data-society/global-climate-change-data. Download "GlobalLandTemperaturesByCountry.csv".
### Tweets:


### Flights:




The above dataset are downloaded and placed into the dataset folder.

## Execution 
Step 1: Install the necessary packages under the package section

Step 2: Download the data listed under data collection to the "dataset" folder

Step 3: Run code/main.py to generate dataset/prediction.csv 

Step 4:
