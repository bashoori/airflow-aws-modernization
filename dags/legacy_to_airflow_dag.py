# Project: Legacy Job Orchestration Modernization with Apache Airflow and AWS

# DAG: legacy_to_airflow_dag.py

# Import required Airflow classes and modules
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
import logging
import requests
import pandas as pd
import boto3
import os

# Default DAG arguments
# These settings define the owner, retry behavior, and notification settings
default_args = {
    'owner': 'bita',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=3)
}

# Task 1: Extract data from a public API and save as CSV
# This simulates pulling raw product data from an external source
def extract_data():
    logging.info("Extracting data from mock API...")
    url = "https://fakestoreapi.com/products"
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    data = response.json()
    df = pd.json_normalize(data)  # Convert JSON to DataFrame
    os.makedirs("/tmp/data", exist_ok=True)
    df.to_csv("/tmp/data/products.csv", index=False)
    logging.info("Data saved to /tmp/data/products.csv")

# Task 2: Transform the raw CSV by adding new columns or formatting
# This simulates a basic ETL transformation stage
def transform_data():
    logging.info("Transforming data...")
    df = pd.read_csv("/tmp/data/products.csv")
    df['price_with_tax'] = df['price'] * 1.12  # Add 12% tax column
    df.to_csv("/tmp/data/products_transformed.csv", index=False)
    logging.info("Transformed data saved to /tmp/data/products_transformed.csv")

# Task 3: Load the transformed CSV into an S3 bucket
# This demonstrates how Airflow can integrate with AWS for storage
def load_to_s3():
    logging.info("Loading data to AWS S3...")
    s3 = boto3.client('s3')
    bucket_name = "your-s3-bucket-name"  # Replace with your real bucket name
    s3.upload_file("/tmp/data/products_transformed.csv", bucket_name, "products_transformed.csv")
    logging.info("Data uploaded to S3 bucket")

# Define the DAG
# The DAG runs daily and orchestrates the ETL process in a clear sequence
with DAG(
    'legacy_to_airflow_dag',
    default_args=default_args,
    description='Migrate legacy Windows jobs to Airflow with AWS integration',
    schedule_interval=timedelta(days=1),  # Run once per day
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['aws', 'airflow', 'etl', 'portfolio']
) as dag:

    # Dummy task to mark the start of the workflow
    start = DummyOperator(task_id='start')

    # Python tasks to run extract, transform, and load
    extract = PythonOperator(task_id='extract_data', python_callable=extract_data)
    transform = PythonOperator(task_id='transform_data', python_callable=transform_data)
    load = PythonOperator(task_id='load_to_s3', python_callable=load_to_s3)

    # Dummy task to mark the end of the workflow
    end = DummyOperator(task_id='end')

    # Set task dependencies in order: start -> extract -> transform -> load -> end
    start >> extract >> transform >> load >> end
