# scripts/extract_transform_load.py

import os
import requests
import pandas as pd
import logging

DATA_DIR = "/opt/airflow/tmp/data"
EXTRACTED_FILE = os.path.join(DATA_DIR, "products.csv")
TRANSFORMED_FILE = os.path.join(DATA_DIR, "products_transformed.csv")


def extract_products_to_csv():
    """
    Extracts product data from a mock API and saves it as a CSV.
    """
    logging.info("Starting data extraction from API...")
    url = "https://fakestoreapi.com/products"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        df = pd.json_normalize(data)

        os.makedirs(DATA_DIR, exist_ok=True)
        df.to_csv(EXTRACTED_FILE, index=False)
        logging.info(f"Data extracted and saved to: {EXTRACTED_FILE}")
    except Exception as e:
        logging.error(f"Failed to extract data: {e}")
        raise


def transform_products_csv():
    """
    Reads the extracted CSV, applies transformations, and saves a new CSV.
    """
    logging.info("Starting data transformation...")

    try:
        df = pd.read_csv(EXTRACTED_FILE)
        df['price_with_tax'] = df['price'] * 1.12  # Add 12% tax
        df.to_csv(TRANSFORMED_FILE, index=False)
        logging.info(f"Transformed data saved to: {TRANSFORMED_FILE}")
    except FileNotFoundError:
        logging.error(f"Extracted file not found at {EXTRACTED_FILE}")
        raise
    except Exception as e:
        logging.error(f"Transformation failed: {e}")
        raise


def get_file_paths():
    """
    Returns dictionary of file paths used in ETL.
    """
    return {
        "extracted_file": EXTRACTED_FILE,
        "transformed_file": TRANSFORMED_FILE
    }