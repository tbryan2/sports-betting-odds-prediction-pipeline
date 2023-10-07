from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from datetime import datetime
import emails

from getSecrets import SecretsManager
from odds import get_odds
from downloadS3Model import download_model_from_s3
from predictOdds import predict_odds
from sesEmail import send_email

with DAG("h2h_pipeline",
    start_date=datetime(2023, 9, 29),
    schedule_interval="@daily",
    catchup=False,
    is_paused_upon_creation=False) as dag:

    t0a = PythonOperator(
        task_id='get_secrets',
        python_callable=SecretsManager().get_secrets,
        provide_context=True,
    )

    t1 = PythonOperator(
        task_id="get_odds",
        python_callable=get_odds,
        provide_context=True,
        op_kwargs={
            "sport": "americanfootball_nfl",
            "regions": "us",
            "bookmakers": "fanduel",
            "odds_format": "american"
        }
    )

    t2 = PythonOperator(
        task_id="download_model_from_s3",
        python_callable=download_model_from_s3,
        op_kwargs={
            "bucket_name": "sportsbettingoddspredictionpipeline",
            "model_key": "models/dummy_model.h5",
            "local_model_path": "/tmp/dummy_model.h5"
        }
    )

    t3 = PythonOperator(
        task_id="predict_odds",
        python_callable=predict_odds,
        op_kwargs={
            "model_path" : "/tmp/dummy_model.h5",
        }
    )

    t4 = PythonOperator(
        task_id="send_email",
        python_callable=send_email,
        provide_context=True,
        op_kwargs={
            "prediction_path": "Users/timothybryan/airflow/dags/data/predictions.csv",
            "body" : "<p>Here are my predictions:</p>",
            "subject" : "NFL Head-to-Head Predictions",
            "mail_from" : "timsfootballs@gmail.com",
            "mail_to" : "timbryan0315@gmail.com"
        }
    )

    t0a >> t1 >> t2 >> t3 >> t4
