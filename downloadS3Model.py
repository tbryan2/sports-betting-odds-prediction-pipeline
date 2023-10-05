import os
import boto3
import requests
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv

def is_running_on_ec2():
    """
    Are we running on an EC2 instance?
    """
    try:
        response = requests.get(
            'http://169.254.169.254/latest/meta-data/instance-id', timeout=1)
        return True
    except requests.exceptions.RequestException:
        return False

def download_model_from_s3(bucket_name, model_key, local_model_path):
    """
    Create a directory called 'models/' and download a model file from an S3 bucket into it.
    """
    # Create 'models/' directory if it does not exist
    if not os.path.exists('/tmp/models'):
        os.makedirs('/tmp/models/')

    load_dotenv()
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    # Initialize S3 client
    if is_running_on_ec2():
        s3 = boto3.client('s3')
    else:
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)

    try:
        # Download the model file from S3 to the local 'models/' directory
        s3.download_file(bucket_name, model_key, local_model_path)
        print(f"Model downloaded from S3 and saved at {local_model_path}")

    except NoCredentialsError:
        print("Credentials not available.")
    except PartialCredentialsError:
        print("Incomplete credentials provided.")
    except Exception as e:
        print(f"An error occurred: {e}")
