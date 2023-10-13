import os
import boto3
import requests
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv

def is_running_on_ec2():
    try:
        # Try to request instance identity document
        response = requests.get('http://169.254.169.254/latest/dynamic/instance-identity/document', timeout=1)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        pass
    return False


def download_model_from_s3(bucket_name, model_key, local_model_path):
    """
    Create a directory called 'models/' and download a model file from an S3 bucket into it.
    """

    # Initialize S3 client
    if is_running_on_ec2():
        s3 = boto3.client('s3')
    else:
        load_dotenv()
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

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

    print(f"Downloaded model should exist at: {local_model_path}")
    print(f"Does it actually exist? {os.path.exists(local_model_path)}")
