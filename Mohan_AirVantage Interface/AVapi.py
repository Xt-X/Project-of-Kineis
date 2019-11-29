#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests, json
from datetime import datetime, timedelta
from dateutil.parser import parse


inited = False
raw_data_url = "https://eu.airvantage.net/api/v1/systems/data/raw?targetIds=beb91e6f88984b27b8fca27506a85cc9&dataIds=MangOH.Sensors.Accelerometer.Acceleration.X,MangOH.Sensors.Accelerometer.Acceleration.Y,MangOH.Sensors.Accelerometer.Acceleration.Z,MangOH.Sensors.Accelerometer.Gyro.X,MangOH.Sensors.Accelerometer.Gyro.Y,MangOH.Sensors.Accelerometer.Gyro.Z,MangOH.Sensors.Light.Level,MangOH.Sensors.Pressure.Pressure,MangOH.Sensors.Pressure.Temperature"



def initCredentials(RO_user, RO_password, client_id, client_secret):
    global inited, tokens
    token_url = "https://eu.airvantage.net/api/oauth/token"
    data = {'grant_type': 'password','username': RO_user, 'password': RO_password}
    access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))
    tokens = json.loads(access_token_response.text)
    inited = True


def getDataForDateRange(from_date, to_date):

    if(inited == False):
        print("initCredentials(...) must be called before using the API")
        return -1
    
    # Converting date into timestamp
    # To match airvantage timestamp - Multiply by 1000 & converting float into int 
    from_timestamp = int((datetime.timestamp(parse(from_date))) * 1000)
    to_timestamp = int((datetime.timestamp(parse(to_date))) * 1000)

    # Append the from - to : date filter to the raw_url
    timestamp_filter = '&from=' + str(from_timestamp) + '&to=' + str(to_timestamp)
    url = raw_data_url + timestamp_filter

    # Calling the API
    api_call_headers = {'Authorization': 'Bearer ' + tokens['access_token']}
    api_call_response = requests.get(url, headers=api_call_headers, verify=False)
    return(api_call_response.text)



def getDataFromNoOfDays(number_of_days):
    
    if(inited == False):
        print("initCredentials(...) must be called before using the API")
        return  -1

    # Converting date into timestamp
    # To match airvantage timestamp - Multiply by 1000 & converting float into int 
    from_timestamp = int((datetime.timestamp(datetime.now() - timedelta(days=number_of_days))) * 1000)

    # Append the from - to : date filter to the raw_url
    timestamp_filter = '&from=' + str(from_timestamp) 
    url = raw_data_url + timestamp_filter

    # Calling the API
    api_call_headers = {'Authorization': 'Bearer ' + tokens['access_token']}
    api_call_response = requests.get(url, headers=api_call_headers, verify=False)
    return(api_call_response.text)
    

