from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from datetime import datetime
import emails

from odds import get_odds
from sesemail import send_email
from keys import SES_HOST_ADDRESS, SES_USER_ID, SES_PASSWORD, ODDS_API_KEY

with DAG("h2h_pipeline", # DAG id
    start_date=datetime(2023, 9, 29),
    schedule_interval="@daily",
    catchup=False) as dag:

    t1 = PythonOperator(
        task_id="get_odds",
        python_callable=get_odds,
        do_xcom_push=False,  # Disable XCom push
        op_kwargs={
            "sport" : "americanfootball_nfl",
            "api_key" : ODDS_API_KEY,
            "regions"  : "us",
            "bookmakers" : "fanduel",
            "odds_format" : "american"
        }
    )

    t2 = PythonOperator(
        task_id="predict",
        python_callable=predict,
        op_kwargs={
            "odds_path" : "data/odds.csv",
            "model_path" : "models/dummy_model.h5"
        }
    )

    t3 = PythonOperator(
        task_id="send_email",
        python_callable=send_email,
        op_kwargs={
            "html" : "<p>Testing email</p>",
            "subject" : "Odds update",
            "mail_from" : "timsfootballs@gmail.com",
            "mail_to" : "timbryan0315@gmail.com",
            "host" : SES_HOST_ADDRESS,
            "user" : SES_USER_ID,
            "password" : SES_PASSWORD
        }
    )

    t1 >> t3
