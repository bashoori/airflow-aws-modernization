# 🛠️ Legacy Job Orchestration Modernization with Apache Airflow and AWS

This project demonstrates how to modernize legacy Windows-scheduled ETL scripts into robust, scalable Apache Airflow DAGs — deployed using Docker and integrated with AWS services like S3 and Redshift.

---
## 📊 Architecture Overview

![Architecture Diagram](https://github.com/bashoori/repo/blob/master/airflow-aws-modernization/airflow-WS-S3-Redshift.png)

---

## 🚀 Features
- Migrate `.bat`/`.py` scripts to Airflow DAGs
- ETL pipeline with extract-transform-load steps
- Data ingestion from public API
- AWS S3 integration
- Dockerized Airflow environment (webserver + scheduler)
- Retry logic, logging, and alerting scaffolding
- Fully documented for learning and reusability

---

## 📁 Folder Structure
```
airflow-aws-modernization/
├── dags/
│   ├── legacy_to_airflow_dag.py         # Main Airflow DAG file
│   └── utilities/
│       └── test_redshift_connection_env.py  # Redshift connection test DAG
├── docker/
│   └── docker-compose.yml               # Airflow Docker deployment
├── scripts/
│   └── extract_transform_load.py        # Optional reusable ETL script
├── redshift/
│   └── create_tables.sql                # Redshift schema setup
├── docs/
│   └── airflow_aws_architecture.png     # Architecture diagram
├── LICENSE                              # MIT license
├── README.md                            # Project documentation
├── .gitignore                           # Ignore rules for Git
├── .env.example                         # Sample AWS credentials (not committed)
└── .github/
    └── workflows/
        └── airflow-lint.yml             # GitHub Actions CI/CD linting setup
        
        
```

## 🧱 Tech Stack
- Apache Airflow 2.7.1 (Dockerized)
- Python 3.9
- PostgreSQL (Airflow backend)
- AWS S3 (data storage)
- Pandas + Requests + Boto3
- psycopg2 (for Redshift connections)  

---

## 🔧 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/airflow-aws-modernization.git
cd airflow-aws-modernization
```

### 2. Set up environment variables
Copy the sample environment file:
```bash
cp .env.example .env
```
Add your AWS credentials to `.env`.

### 3. Start Airflow with Docker Compose
```bash
cd docker
docker-compose up -d
```

### 4. Access the Airflow UI
Go to [http://localhost:8080](http://localhost:8080) and enable the `legacy_to_airflow_dag`.

---

## 🗂️ DAG Tasks Overview

🔹 Main DAG: legacy_to_airflow_dag.py
- **Extract**: Pull product data from a public API
- **Transform**: Add derived fields (e.g., tax-calculated price)
- **Load**: Upload CSV to AWS S3 bucket

🔹 Utility DAG: test_redshift_connection_env.py
This DAG validates that Airflow can successfully connect to an AWS Redshift cluster using credentials stored in a `.env` file.

	•	Uses psycopg2 to run a simple test query
	•	Logs success/failure with retry and timeout
	•	Confirms Redshift connectivity before deploying full pipelines

---

## 🧠 About the Author
Built by **Bita Ashoori** — Data Engineer & Automation Enthusiast



