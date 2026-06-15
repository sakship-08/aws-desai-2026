import json
import boto3

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('VisitorCount')

def lambda_handler(event, context):
    # 1. Increment the 'count' for the item with id='visitors'
    response = table.update_item(
        Key={'id': 'visitors'},
        UpdateExpression='ADD #c :val',
        ExpressionAttributeNames={'#c': 'count'},
        ExpressionAttributeValues={':val': 1},
        ReturnValues="UPDATED_NEW"
    )
    
    # 2. Get the new count
    new_count = response['Attributes']['count']

    # 3. Return the count with CORS headers
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*', # Required for your website to talk to the API
            'Access-Control-Allow-Methods': 'GET'
        },
        'body': json.dumps({'count': int(new_count)})
    }
