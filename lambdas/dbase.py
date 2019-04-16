import boto3
import json
import decimal

dynamodb = boto3.resource('dynamodb')

# function from https://github.com/boto/boto3/issues/665
def round_float_to_decimal(float_value):
    """
    Convert a floating point value to a decimal that DynamoDB can store,
    and allow rounding.
    """

    # Perform the conversion using a copy of the decimal context that boto3
    # uses. Doing so causes this routine to preserve as much precision as
    # boto3 will allow.
    with decimal.localcontext(boto3.dynamodb.types.DYNAMODB_CONTEXT) as \
         decimalcontext:

        # Allow rounding.
        decimalcontext.traps[decimal.Inexact] = 0
        decimalcontext.traps[decimal.Rounded] = 0
        decimal_value = decimalcontext.create_decimal_from_float(float_value)
        # g_logger.debug("float: {}, decimal: {}".format(float_value,
        #                                                decimal_value))

        return decimal_value
        
def lambda_handler(event, context):
    print('API event JSON:' + json.dumps(event))
    table = dynamodb.Table('weatherRecords')

    itemId = event['date']  # date string in ISO 8601 format
    minTemp = event['min']  # string temp in F
    maxTemp = event['max']  # string temp in F
    precip = event['precip']  # string ppt in inches
    
    # for some stupid reason, DynamoDB can't hadle floating point numbers, so I'm saving them as strings        
    response = table.put_item(
        Item={
            'isoDate': itemId,
            'min': minTemp,
            'max': maxTemp,
            'ppt': precip
        }
    )

    print('Database response: '+ str(response))
    return response
    