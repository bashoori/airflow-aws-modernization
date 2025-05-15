# Project: Legacy Job Orchestration Modernization with Apache Airflow and AWS

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
import logging
import requests
import pandas as pd
import boto3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='/opt/airflow/.env')

# Default DAG arguments
default_args = {
    'owner': 'bita',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=3)
}

# Shared data path (Airflow container-safe)
DATA_DIR = "/opt/airflow/tmp/data"
EXTRACTED_FILE = f"{DATA_DIR}/products.csv"
TRANSFORMED_FILE = f"{DATA_DIR}/products_transformed.csv"

def extract_data():
    logging.info("Extracting data from mock API...")
    url = "https://fakestoreapi.com/products"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    df = pd.json_normalize(data)
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(EXTRACTED_FILE, index=False)
    logging.info(f"Data saved to {EXTRACTED_FILE}")

def transform_data():
    logging.info("Transforming data...")
    df = pd.read_csv(EXTRACTED_FILE)
    df['price_with_tax'] = df['price'] * 1.12
    df.to_csv(TRANSFORMED_FILE, index=False)
    logging.info(f"Transformed data saved to {TRANSFORMED_FILE}")

def load_to_s3():
    logging.info("Loading data to AWS S3...")
    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_DEFAULT_REGION", "us-west-2")
    bucket_name = os.getenv("S3_BUCKET_NAME")

    if not all([aws_key, aws_secret, bucket_name]):
        raise ValueError("Missing AWS credentials or S3_BUCKET_NAME in .env file")

    s3 = boto3.client('s3',
                      aws_access_key_id=aws_key,
                      aws_secret_access_key=aws_secret,
                      region_name=aws_region)

    s3.upload_file(TRANSFORMED_FILE, bucket_name, "products_transformed.csv")
    logging.info("Data uploaded to S3 successfully")

with DAG(
    'legacy_to_airflow_dag',
    default_args=default_args,
    description='Migrate legacy Windows jobs to Airflow with AWS integration',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['aws', 'airflow', 'etl', 'portfolio']
) as dag:

    start = DummyOperator(task_id='start')
    extract = PythonOperator(task_id='extract_data', python_callable=extract_data)
    transform = PythonOperator(task_id='transform_data', python_callable=transform_data)
    load = PythonOperator(task_id='load_to_s3', python_callable=load_to_s3)
    end = DummyOperator(task_id='end')

    start >> extract >> transform >> load >> end