#!/bin/bash
# Initialize the database
pip install boto3 pandas requests emails python-dotenv tensorflow

airflow db init

# Create the user
airflow users create \
    --username admin \
    --password admin \
    --firstname Anonymous \
    --lastname User \
    --role Admin \
    --email admin@example.org

# Download the tasks.zip from S3
aws s3 cp s3://sportsbettingoddspredictionpipeline/dags/tasks.zip /opt/airflow/tasks.zip

# Unzip the tasks into a temporary directory
unzip /opt/airflow/tasks.zip -d /opt/airflow/temp_tasks/

# Move the DAG files to the dags directory
mv /opt/airflow/temp_tasks/tasks/* /opt/airflow/dags/

# Remove the temporary directory
rm -r /opt/airflow/temp_tasks/

# Run pipeline.py to ensure it's picked up by the scheduler
python /opt/airflow/dags/pipeline.py

# Run the scheduler in the background
airflow scheduler &
airflow webserver &

# Wait for the scheduler to fully start (you can adjust the sleep time)
sleep 10

# Trigger the DAG run
airflow dags trigger h2h_pipeline

# Keep the script running (this could be necessary depending on how your Docker container is set up)
wait