import os
import json
import boto3
from botocore.exceptions import ClientError

def get_secrets():
    '''
    Fetch secrets and return them as a Python dictionary
    '''
    secret_name = "SportsBettingOddsPredictionPipelineSecrets"
    region_name = "us-east-1"

    # Get AWS credentials from environment variables
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as exception:
        raise exception

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    secret_dict = json.loads(secret)
    
    return secret_dict
