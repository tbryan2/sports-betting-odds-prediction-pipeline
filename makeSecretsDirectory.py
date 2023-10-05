import os

# Function to make directory
def make_secrets_dir():
    '''
    Create directory for secrets
    '''
    dir_path = 'secrets'
    os.makedirs(dir_path, exist_ok=True)
