# 🛠️ Legacy Job Orchestration Modernization with Apache Airflow and AWS

This project demonstrates how to modernize legacy Windows-scheduled ETL scripts into robust, scalable Apache Airflow DAGs — deployed using Docker and integrated with AWS services like S3 and Redshift.

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
│   └── legacy_to_airflow_dag.py         # Your main DAG file (with comments)
├── docker/
│   └── docker-compose.yml               # Airflow deployment config
├── scripts/
│   └── extract_transform_load.py        # Reusable ETL logic (optional)
├── redshift/
│   └── create_tables.sql                # SQL DDL to prepare Redshift table
├── docs/
│   └── airflow_aws_architecture.png     # Architecture diagram (to be created)
├── LICENSE                              # MIT license file
├── README.md                            # Full project documentation
├── .gitignore                           # With Python, Airflow, Docker exclusions
└── .env.example                         # Placeholder for AWS credentials (not tracked)
```

## 🧱 Tech Stack
- Apache Airflow 2.7.1 (Dockerized)
- Python 3.9
- PostgreSQL (Airflow backend)
- AWS S3 (data storage)
- Pandas + Requests + Boto3

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
- **Extract**: Pull product data from a public API
- **Transform**: Add derived fields (e.g., tax-calculated price)
- **Load**: Upload CSV to AWS S3 bucket

---

## 📊 Architecture
> Diagram available at: `docs/airflow_aws_architecture.png` (to be added)

---

## 🧠 About the Author
Built with ❤️ by **Bita Ashoori** — Data Engineer & Automation Enthusiast

---

## 📄 License
Licensed under the [MIT License](LICENSE).

