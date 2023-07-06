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
conn = sqlite3.connect('/home/sdc/www/django_apps/myapp/SDC_project.sqlite3')
cur = conn.cursor() 

##########################
#### Data Preparation ####
##########################

# Opening JSON file
rf = json.load(open('/home/sdc/www/django_apps/weather_data/rf_laos.json'))
rh = json.load(open('/home/sdc/www/django_apps/weather_data/rh_laos.json'))
tmax = json.load(open('/home/sdc/www/django_apps/weather_data/tmax_laos.json'))
tmin = json.load(open('/home/sdc/www/django_apps/weather_data/tmin_laos.json'))
ws = json.load(open('/home/sdc/www/django_apps/weather_data/ws_laos.json'))

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
wf2 = pd.DataFrame(c_list, columns=['date_data', 'province_name', 'rainfall', 'humidity', 'max_temp', 'min_temp', 'windspeed'])

# Read data in database and convert to dataframe
sql_query = pd.read_sql_query (''' SELECT * FROM weather_forecast_laos ''', conn)
db_table = pd.DataFrame(sql_query)

# Create new weather forecast dataframe from lastest date of database
# Since <class 'datetime.date'> cannot use with > , So we have to change date type
wf['date_data'] = pd.to_datetime(wf['date_data'], format='%Y-%m-%d')
last_db_date = pd.to_datetime(db_table['date_data'].iloc[-1], format='%Y-%m-%d')
filtered_wf = wf.loc[(wf['date_data'] > last_db_date)]
# Change date type back to <class 'datetime.date'>
filtered_wf['date_data'] = pd.to_datetime(filtered_wf['date_data']).apply(lambda x: x.date())
# Update the duplicate data in database
for index, row in wf2.iterrows():
  cur.execute(''' UPDATE weather_forecast_laos SET rainfall = ?, humidity = ?, max_temp = ?, 
  min_temp = ?, windspeed = ?  WHERE date_data = ? AND province_name = ? ;''', (row['rainfall'], row['humidity'], row['max_temp'], 
                                                         row['min_temp'], row['windspeed'], row['date_data'], row['province_name']))
  conn.commit()

##########################################
#### Get from Pandas DataFrame to SQL ####
##########################################

filtered_wf.to_sql(name='weather_forecast_laos', con=conn, if_exists='append', index=False)
conn.commit()

cur.execute("SELECT * FROM weather_forecast_laos ORDER BY id DESC LIMIT 15")
for row in cur.fetchall():
    print (row)
