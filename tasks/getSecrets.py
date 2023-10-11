from dotenv import load_dotenv
import os
import json
import boto3
import requests
from botocore.exceptions import ClientError


class SecretsManager:
    '''
    Load secrets for sports betting odds prediction pipeline
    from AWS Secrets Manager, using access keys if local and
    forgoing them if running on EC2.
    '''

    def __init__(self):
        load_dotenv()
        self.secret_name = "SportsBettingOddsPredictionPipelineSecrets"
        self.region_name = "us-east-1"
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    def is_running_on_ec2(self):
        '''
        Are we running on EC2?
        '''
        # Check if AWS_DEFAULT_REGION environment variable is set
        if os.environ.get("AWS_DEFAULT_REGION"):
            return True

        # Check if the username is 'ec2-user'
        my_user = os.environ.get("USER")
        if "ec2-user" in my_user:
            return True

        return False

    def get_client(self):
        '''
        Load AWS Secrets Manager client, using access keys if local and
        forgoing them if running on EC2.
        '''
        if self.is_running_on_ec2():
            return boto3.client('secretsmanager', region_name=self.region_name)
        else:
            session = boto3.session.Session()
            return session.client(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                service_name='secretsmanager',
                region_name=self.region_name
            )

    def get_secrets(self, **kwargs):
        '''
        Load secrets from AWS Secrets Manager, using access keys if local and
        forgoing them if running on EC2. Push to XCom if task_instance is
        available in kwargs.
        '''
        client = self.get_client()
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=self.secret_name)
        except ClientError as exception:
            raise exception

        secret = get_secret_value_response['SecretString']
        secret_dict = json.loads(secret)

        # Push to XCom if task_instance is available in kwargs
        if 'ti' in kwargs:
            kwargs['ti'].xcom_push(key='secrets', value=secret_dict)

        return secret_dict
