from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from datetime import datetime
import emails

from getSecrets import get_secrets
from odds import get_odds
from predictOdds import predict_odds
from sesEmail import send_email
from keys import SES_HOST_ADDRESS, SES_USER_ID, SES_PASSWORD, ODDS_API_KEY

with DAG("h2h_pipeline",
    start_date=datetime(2023, 9, 29),
    schedule_interval="@daily",
    catchup=False) as dag:

    t0a = PythonOperator(
        task_id='get_secrets',
        python_callable=get_secrets,
    )

    t1 = PythonOperator(
        task_id="get_odds",
        python_callable=get_odds,
        provide_context=True,
        op_kwargs={
            "sport" : "americanfootball_nfl",
            "api_key" : ODDS_API_KEY,
            "regions"  : "us",
            "bookmakers" : "fanduel",
            "odds_format" : "american",
            "csv_save_path" : "Users/timothybryan/airflow/dags/data/odds.csv"
        }
    )

    t2 = PythonOperator(
        task_id="predict_odds",
        python_callable=predict_odds,
        op_kwargs={
            "odds_path": "Users/timothybryan/airflow/dags/data/odds.csv",
            "model_path" : "Users/timothybryan/airflow/dags/models/dummy_model.h5",
            "prediction_path": "Users/timothybryan/airflow/dags/data/predictions.csv"
        }
    )

    t3 = PythonOperator(
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

    t0a >> t1 >> t2 >> t3
