import json
import boto3

def lambda_handler(event, context):
    print("Iam in the function")
    print(event)
    user=event['user_id']
    email=event['email_id']
    verify_email_identity(email)
    performUserEmailops(user,email)
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('User Created Succesfully')
    }


def create_user(user_id, email):
    user = {
        'user_id':user_id ,
        'email':email
    }
    return user;
    
def performUserEmailops(user_id, email):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('notifusers')
    user=create_user(user_id, email)
    table.put_item(Item=user)

def create_table_with_gsi():
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.create_table(
        TableName='notifusers',
        KeySchema=[
            {
                'AttributeName': 'user_id',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'user_id',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            },
    
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'email',
                'KeySchema': [
                    {
                        'AttributeName': 'email',
                        'KeyType': 'HASH'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput' :{
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1,
                }
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1,
        }
    )

    print("Table status:", table.table_status)
    
def verify_email_identity(email_id):
    ses_client = boto3.client("ses", region_name="us-east-2")
    response = ses_client.verify_email_identity(
        EmailAddress=email_id
    )
    print(response)
