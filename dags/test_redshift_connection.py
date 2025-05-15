from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import psycopg2
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv(dotenv_path='/opt/airflow/.env')

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

def test_redshift_connection():
    logging.info("Testing Redshift connection using .env credentials...")

    conn = psycopg2.connect(
        host=os.getenv("REDSHIFT_HOST"),
        dbname=os.getenv("REDSHIFT_DB"),
        user=os.getenv("REDSHIFT_USER"),
        password=os.getenv("REDSHIFT_PASSWORD"),
        port=os.getenv("REDSHIFT_PORT", 5439)
    )
    
    cur = conn.cursor()
    cur.execute('SELECT 1;')
    result = cur.fetchone()
    logging.info(f"Redshift Test Query Result: {result}")
    cur.close()
    conn.close()

with DAG(
    dag_id='test_redshift_connection_env',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['test', 'redshift'],
) as dag:

    test_conn = PythonOperator(
        task_id='test_env_redshift_connection',
        python_callable=test_redshift_connection
    )