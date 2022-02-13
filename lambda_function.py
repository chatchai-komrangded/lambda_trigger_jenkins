import requests
import json
import os
import boto3
import base64
import time
import pytz
from botocore.exceptions import ClientError
from datetime import datetime

jenkin_url = os.environ['jenkin_url']
jenkinpipeline_name = os.environ['jenkinpipeline_name']
auth_token = os.environ['auth_token']
secret_name = os.environ['secret_name']
region_name = os.environ['region_name']
tz = pytz.timezone('Asia/Bangkok')


def get_secret():

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            return base64.b64decode(get_secret_value_response['SecretBinary'])
            
def get_secret_value(secert_string):
    # secert json is of format {'key' : 'value'}
    secert_json = json.loads(secert_string)
    # Get values
    return list(secert_json.values())[0]


def lambda_handler(event, context):   
    user_api_token = json.loads(get_secret())
    user = list(user_api_token.keys())[0]
    api_token = user_api_token[user]
    url = 'http://'+user+':'+api_token+'@'+ jenkin_url + jenkinpipeline_name + '/buildWithParameters?token=' + auth_token
    try:
        r = requests.post(url)
        now = datetime.now(tz)
        print (now.strftime("%Y-%m-%d %H:%M:%S"))
        print("Successful trigger jenkin pipeline: " + jenkinpipeline_name + " at "+now.strftime("%Y-%m-%d %H:%M:%S"))
    except Exception as e:
        print("Error conntection to jenkin pipelines "+e)

'''
if __name__ == "__main__":
    event = []
    context = []
    lambda_handler(event, context)
'''    
  

    
    