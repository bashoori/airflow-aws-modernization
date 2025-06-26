from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import psycopg2
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv(dotenv_path='/opt/airflow/.env')

# Set up structured logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Default args
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

def test_redshift_connection():
    logger.info("Testing Redshift connection using .env credentials...")
    try:
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
        logger.info(f"Redshift Test Query Result: {result}")
        cur.close()
        conn.close()
    except Exception as e:
        logger.exception("Redshift connection failed.")
        raise

# DAG definition
with DAG(
    dag_id='test_redshift_connection_env',
    default_args=default_args,
    description='Test Redshift connection using credentials from .env file',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['test', 'redshift'],
) as dag:

    test_conn = PythonOperator(
        task_id='test_env_redshift_connection',
        python_callable=test_redshift_connection,
        execution_timeout=timedelta(minutes=5),
        retries=1,
        retry_exponential_backoff=True
    )