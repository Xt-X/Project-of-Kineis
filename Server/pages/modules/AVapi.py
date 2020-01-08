#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests, json
from datetime import datetime, timedelta


sensor_data_raw_bulk = (
    "https://eu.airvantage.net/api/v1/systems/data/raw?targetIds=beb91e6f88984b27b8fca27506a85cc9&dataIds=MangOH.Sensors.Accelerometer.Acceleration.X,"
    "MangOH.Sensors.Accelerometer.Acceleration.Y,"
    "MangOH.Sensors.Accelerometer.Acceleration.Z,"
    "MangOH.Sensors.Accelerometer.Gyro.X,"
    "MangOH.Sensors.Accelerometer.Gyro.Y,"
    "MangOH.Sensors.Accelerometer.Gyro.Z,"
    "MangOH.Sensors.Pressure.Temperature,"
    "MangOH.Sensors.Pressure.Pressure,"
    "MangOH.Sensors.Light.Level&size=500")

inited = False

# Step A - resource owner supplies credentials
token_url = "https://eu.airvantage.net/api/oauth/token"
RO_user = "smohanp18@gmail.com"
RO_password = "#$Kineis2020"
client_id = '847ec44018f442538b3d342c0b08fe44'
client_secret = '3b9c1a5b47ab4bcc8dfdd04acfa6c08e'

def initCredentials(RO_user, RO_password, client_id, client_secret):
    global inited, api_call_headers
    if(inited == True):
        return 1
    token_url = "https://eu.airvantage.net/api/oauth/token"
    data = {'grant_type': 'password','username': RO_user, 'password': RO_password}
    access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))
    tokens = json.loads(access_token_response.text)
    api_call_headers = {'Authorization': 'Bearer ' + tokens['access_token']}
    inited = True



def airvantageRange(dateFrom,dateTo):

    if(inited == False):
        print("initCredentials(...) must be called before using the API")
        return  -1

    timestampFrom = str(int(datetime.fromisoformat(dateFrom).timestamp()) * 1000)
    timestampTo = str((int(datetime.fromisoformat(dateTo).timestamp())) * 1000)

    crafted_url = sensor_data_raw_bulk + "&from=" +timestampFrom + "&to="+timestampTo
    return airvantageCall(crafted_url)


def airvantageNbDays(nbDays):

    if(inited == False):
        print("initCredentials(...) must be called before using the API")
        return  -1

    timestampFrom = str(int((datetime.timestamp(datetime.now() - timedelta(days=int(nbDays)))) * 1000))

    crafted_url = sensor_data_raw_bulk + "&from=" + timestampFrom
    return airvantageCall(crafted_url)


def airvantageCall(resource_url):

    api_call_response = requests.get(resource_url, headers=api_call_headers, verify=False)
    datas = json.loads(api_call_response.text)

    tempDic = {}
    if "beb91e6f88984b27b8fca27506a85cc9" not in datas.keys():
        return {}
    for i in datas["beb91e6f88984b27b8fca27506a85cc9"]:
        d = {}
        for (index, value) in enumerate(datas["beb91e6f88984b27b8fca27506a85cc9"][i]):
            newKey = value["ts"]
            newValue = value["v"]
            d[newKey] = newValue
        tempDic[i] = d
    return tempDic
