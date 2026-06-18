import json, time, boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Attendance')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    now = int(time.time())

    if body['expiresAt'] < now:
        return response(400, "QR expired")

    table.put_item(
        Item={
            "studentId": body["studentId"],
            "classDate": body["classDate"],
            "name": body["name"],
            "subject": body["subject"],
            "timestamp": now
        },
        ConditionExpression="attribute_not_exists(studentId)"
    )

    return response(200, "Attendance marked")

def response(code, msg):
    return {
        "statusCode": code,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({"message": msg})
    }
