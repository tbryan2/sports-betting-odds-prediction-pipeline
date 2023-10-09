# Use the official Apache Airflow image as the base
FROM apache/airflow:2.1.2

# Switch to root to be able to install packages
USER root

# Install dependencies (add more as needed)
RUN pip install --no-cache-dir apache-airflow boto3 pandas requests emails python-dotenv

# Install unzip and AWS CLI
RUN apt-get update && apt-get install -y unzip awscli

# Switch back to airflow user
USER airflow

# Set the working directory
WORKDIR /opt/airflow

# Copy entrypoint script into the image
COPY entrypoint.sh /entrypoint.sh

# Use the entrypoint script as the entrypoint
ENTRYPOINT ["/entrypoint.sh"]
