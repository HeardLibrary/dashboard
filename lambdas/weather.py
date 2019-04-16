import requests
import boto3
import json
import os
import datetime

def lambda_handler(event, context):
    locationString = '16133_PC' # Pleasant View, TN 37146
    apiKey = 'insert_here'
    url = 'http://dataservice.accuweather.com/currentconditions/v1/' + locationString
    r = requests.get(url, params={'apikey': apiKey, 'details': 'true'})
    data = r.json()
    hasPpt = data[0]['HasPrecipitation'] # value is boolean
    pptInches = data[0]['PrecipitationSummary']['Past24Hours']['Imperial']['Value'] # value is float, I think
    print(datetime.datetime.utcnow().isoformat())
    print(str(hasPpt) + ' Inches precipitation in past 24 hours: ' + str(pptInches))
    