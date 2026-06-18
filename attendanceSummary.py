import json, boto3
from collections import defaultdict

table = boto3.resource('dynamodb').Table('Attendance')

def lambda_handler(event, context):
    items = table.scan()["Items"]
    total_classes = 10

    count = defaultdict(int)
    names = {}

    for i in items:
        count[i["studentId"]] += 1
        names[i["studentId"]] = i["name"]

    summary = [
        {
            "studentId": sid,
            "name": names[sid],
            "percentage": round((c / total_classes) * 100, 2)
        }
        for sid, c in count.items()
    ]

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(summary)
    }
