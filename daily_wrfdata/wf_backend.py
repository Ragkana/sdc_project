from dataclasses import replace
import sqlite3
from xmlrpc.client import Fault
from numpy import append
import pandas as pd
import json
import sys
from datetime import date
import datetime as dt

#############################
#### Connect to database ####
#############################
conn = sqlite3.connect('D:/Django/SDC/SDC_project.SQLite3')
cur = conn.cursor() 
# Test by take a look at weather forecast cambodia table
"""with conn:    
    cur = conn.cursor()    
    cur.execute("SELECT * FROM weather_forecast_laos LIMIT 5")
    rows = cur.fetchall()
    for row in rows:
        print(row)
input()"""

##########################
#### Data Preparation ####
##########################

# Opening JSON file
rf = json.load(open('D:/Django/SDC/Backend_Code/wf_data/rf_06022023_laos.json'))
rh = json.load(open('D:/Django/SDC/Backend_Code/wf_data/rh_06022023_laos.json'))
tmax = json.load(open('D:/Django/SDC/Backend_Code/wf_data/tmax_06022023_laos.json'))
tmin = json.load(open('D:/Django/SDC/Backend_Code/wf_data/tmin_06022023_laos.json'))
ws = json.load(open('D:/Django/SDC/Backend_Code/wf_data/ws_06022023_laos.json'))

###############################
#### Get All data as lists ####
###############################

### Start With Rainfall Data ###
# Create empty list
province = []
rainfall = []
dates = []

# Get all province name
province_raw_rf = rf['r_data']

# Collect data in each list
for p in province_raw_rf:
  for r in rf['r_data'][p]['value']:
    province.append(p)
    rainfall.append(r)
  for d in rf['r_data'][p]['time']:
    dates.append(d)

## We have to handle date&time before combine all lists ##
# 1. We need only start date
dates = [i[0] for i in dates]
# 2. Change data type (string --> date)
# Change format (string --> date) 
day = []
for i in dates:
  result = dt.datetime.strptime(i, '%Y-%m-%dT%XZ').date()
  day.append(result)

### Relative Humidity Data ###
hum = []
province_raw_rh = rh['r_data']

for p in province_raw_rh:
  for a in rh['r_data'][p]['value']:
    hum.append(a)

### Max Temperature Data ###
max_temp = []
province_raw_tmax = tmax['r_data']

for p in province_raw_tmax:
  for b in tmax['r_data'][p]['value']:
    max_temp.append(b)

### Min Temperature Data ###
min_temp = []
province_raw_tmin = tmin['r_data']

for p in province_raw_tmin:
  for c in tmin['r_data'][p]['value']:
    min_temp.append(c)

### Wind Speed Data ###
windspeed = []
province_raw_ws = ws['r_data']

for p in province_raw_ws:
  for d in ws['r_data'][p]['value']:
    windspeed.append(d)

###############################
#### Combination all lists ####
###############################
c_list = list(zip(day, province, rainfall, hum, max_temp, min_temp, windspeed))
wf = pd.DataFrame(c_list, columns=['date_data', 'province_name', 'rainfall', 'humidity', 'max_temp', 'min_temp', 'windspeed'])
print(wf.head(5))

##########################################
#### Get from Pandas DataFrame to SQL ####
##########################################
wf.to_sql(name='weather_forecast_laos', con=conn, if_exists='append', index=False)
conn.commit()

cur.execute("SELECT * FROM weather_forecast_laos ORDER BY id DESC LIMIT 15")
for row in cur.fetchall():
    print (row)


