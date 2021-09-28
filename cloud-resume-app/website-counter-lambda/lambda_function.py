import boto3
import json
import decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('mark-cloud-resume-webVisit-dynamoDB')

# DynamoDB storing floats as Decimals which are not able to be encoded by json.dumps(). 
# To get around this, you can convert Decimals from DynamoDB to floats before encoding into JSON using json.dumps(). 
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def getItem(myTable, hashKey):
    response = myTable.get_item(
        Key = {
            'webVisit_count_type': hashKey
        }
    )
    return response

def checkItemExist(myResponse):
    if 'Item' in myResponse:
        return True
    else:
        return False

def putDefaultItem(myTable, hashKey):
    if hashKey == 'totalVisit':
        myTable.put_item(
            Item={
                'webVisit_count_type': 'totalVisit',
                'visit_counts': 0
            }
        )

def incrementTotalVisit(myTable):
    response = myTable.update_item(
        Key = {
            'webVisit_count_type': 'totalVisit'
        },
        UpdateExpression = 'SET visit_counts = visit_counts + :val',
        ExpressionAttributeValues = {
            ':val': 1
        },
        ReturnValues="ALL_NEW"
    )
    return response



def lambda_handler(event, context):    
    # Add totalVisit into table if doesn't exist
    dynamodbResponse = getItem(table, 'totalVisit')
    isTotalVisitExist = checkItemExist(dynamodbResponse)
    if isTotalVisitExist == False:
        putDefaultItem(table, 'totalVisit')
    
    # Increase the visit_counts of totalVisit by 1   
    dynamodbResponse = incrementTotalVisit(table)


    # Format body of API response with updated visit_counts of totalVisit
    apiResponseBody = json.dumps({"totalVisits": dynamodbResponse["Attributes"]["visit_counts"]}, cls=DecimalEncoder)

    # Return API response
    return {
        "statusCode": 200,
        "isBase64Encoded": False,
        "headers": {
            'Content-Type': "application/json",
            'Access-Control-Allow-Headers': "Content-Type",
            'Access-Control-Allow-Origin': "https://www.markchentp.com"
        },
        "body": apiResponseBody
    }