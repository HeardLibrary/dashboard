import requests
import boto3
import json
import os
import datetime
import pytz

def lambda_handler(event, context):
    locationString = '16133_PC' # Pleasant View, TN 37146
    apiKey = 'oGvDaLfsclkNGva8UoAV11WbAlQpq0N8'
    url = 'http://dataservice.accuweather.com/currentconditions/v1/' + locationString
    r = requests.get(url, params={'apikey': apiKey, 'details': 'true'})
    data = r.json()
    # create datetime object with UTC timezone
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    # convert the datetime object to US Central time zone
    central_now = utc_now.astimezone(pytz.timezone("US/Central"))
    now_iso = central_now.isoformat()
    isoDate = now_iso[0:10]
    pptInches = data[0]['PrecipitationSummary']['Past24Hours']['Imperial']['Value'] # value is float, I think
    minTempF = data[0]['TemperatureSummary']['Past24HourRange']['Minimum']['Imperial']['Value'] # value is float, in deg F
    maxTempF = data[0]['TemperatureSummary']['Past24HourRange']['Maximum']['Imperial']['Value'] # value is float, in deg F
    print(now_iso)
    print(' Min temp in past 24 hours: ' + str(minTempF))
    print(' Max temp in past 24 hours: ' + str(maxTempF))
    print(' Inches precipitation in past 24 hours: ' + str(pptInches))
    outputStruct = {'date': isoDate, 'min': str(minTempF), 'max': str(maxTempF), 'precip': str(pptInches)}
    return outputStruct
    