# Use the official Apache Airflow image as the base
FROM apache/airflow:2.1.2

# Install dependencies (add more as needed)
RUN pip install --no-cache-dir boto3 pandas requests emails python-dotenv

# Declare the build-time variables for AWS keys
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

# Set the environment variables for AWS keys
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}

# Switch to root to be able to install packages
USER root

# Install unzip and AWS CLI
RUN apt-get update && apt-get install -y unzip awscli

# Switch back to airflow user
USER airflow

# Setup Airflow database and user
RUN airflow db init
RUN airflow users create \
    --username admin \
    --password admin \
    --firstname Anonymous \
    --lastname User \
    --role Admin \
    --email admin@example.org

# Set the working directory
WORKDIR /opt/airflow

# Download the tasks.zip file from S3 and unzip it into the 'dags' directory
# Credentials are supposed to be loaded via --env-file in `docker run`
RUN aws s3 cp s3://sportsbettingoddspredictionpipeline/tasks.zip ./tasks.zip && \
    unzip tasks.zip -d dags/

# Run the scheduler
CMD ["airflow", "scheduler"]
