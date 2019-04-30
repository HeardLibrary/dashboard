import os
import boto3
import numpy as np
from bokeh.plotting import figure, output_file, save

# instantiate outside of handler to allow it to be accessible to the lambda for the lambda's lifetime
dynamodb = boto3.resource('dynamodb')

def sortFunction(x):
    return x['isoDate']

def lambda_handler(event, context):
    os.chdir('/tmp')
    
    table = dynamodb.Table('weatherRecords')
    response = table.scan()
    items = response["Items"]
    items.sort(key=sortFunction)
    
    x=[]
    y=[]
    z=[]
    for index in range(len(items)):
        x.append(index)
        y.append(float(items[index]['min']))
        z.append(float(items[index]['max']))
    
    # output to static HTML file
    output_file("lines.html")
    
    # create a new plot with a title and axis labels
    p = figure(title="Pleasant View, Tennessee", x_axis_label='day', y_axis_label='temperature')
    
    # add a line renderer with legend and line thickness
    p.line(x, y, legend="Min.", line_color="blue", line_width=2)
    p.line(x, z, legend="Max.", line_color="red", line_width=2)
    
    # save the results
    save(p, filename='plot.html', title='weather data')

    with open('plot.html', 'rt', encoding='utf-8') as fileObject:
        outString = fileObject.read()

    bucket_name = 'baskauf-bokeh'
    file_name = 'plot.html'
    folder = ''
    s3_path = folder + file_name

    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=outString, ContentType='text/html')
    