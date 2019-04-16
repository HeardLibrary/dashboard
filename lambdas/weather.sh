#!/bin/bash

aws lambda create-function --region us-east-2 --function-name weather_viz --zip-file fileb://zips/weather.zip --role arn:aws:iam::555751041262:role/vizTest_dashboard --handler weather.lambda_handler --runtime python3.7 --memory-size 512
