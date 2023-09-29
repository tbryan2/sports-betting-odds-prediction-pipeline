from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from datetime import datetime

from odds import get_odds
from keys import ODDS_API_KEY

with DAG("h2h_pipeline", # DAG id
    start_date=datetime(2023, 9, 29),
    schedule="@daily",
    catchup=False) as dag:

    t1 = PythonOperator(
        task_id="get_odds",
        python_callable=get_odds,
        op_kwargs={
            "sport" : "americanfootball_nfl",
            "api_key" : ODDS_API_KEY,
            "regions"  : "us",
            "bookmakers" : "fanduel",
            "odds_format" : "american"
        }
    )

