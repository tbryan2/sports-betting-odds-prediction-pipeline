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
        self.secret_name = "SportsBettingOddsPredictionPipelineSecrets"
        self.region_name = "us-east-1"

        if not self.is_running_on_ec2():
            load_dotenv()
            self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
            self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        else:
            self.aws_access_key_id = None
            self.aws_secret_access_key = None


    def is_running_on_ec2(self):
        try:
            # Try to request instance identity document
            response = requests.get('http://169.254.169.254/latest/dynamic/instance-identity/document', timeout=1)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
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
