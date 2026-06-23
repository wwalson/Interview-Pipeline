# Multi-Source ETL Pipeline

## Overview

This project demonstrates a production-style ETL pipeline built using Python, SQL Server, and Git.

The pipeline extracts economic data from external APIs, performs data validation and transformation, loads data into a structured SQL Server warehouse, and prepares data for analytics consumption.

## Architecture
API Sources
|
v
Python ETL Pipeline
|
v
Raw Data Layer
|
v
Quality Checks
|
v
Staging Layer
|
v
Analytics Layer
|
v
Power BI / Streamlit


## Technologies

- Python
- SQL Server
- Pandas
- Requests
- PyODBC
- Git/GitHub
- Power BI
- Streamlit
- dbt (planned)

## Current Pipeline

### Data Source

Federal Reserve Economic Data (FRED) API

Current datasets:

- Federal Funds Rate
- Unemployment Rate
- Consumer Price Index

### Pipeline Features

- API ingestion
- Batch tracking
- Pipeline run IDs
- Data validation
- Null handling
- Parameterized SQL inserts
- Raw data storage
- SQL Server loading

## Project Structure
Pipeline Interview/

├── src/
│ ├── ingestion/
│ │ └── fred_ingestion.py
│ │
│ └── common/
│ ├── config.py
│ └── db.py
│
├── sql/
├── tests/
├── config/
├── logs/
│
├── requirements.txt
└── README.md


## Running the Pipeline

Activate the environment:
conda activate interview_pipeline


Run:
python -m src.ingestion.fred_ingestion


## Future Enhancements

- ETL audit logging
- Automated data quality framework
- Additional API sources
- dbt transformations
- Workflow orchestration
- Power BI dashboard integration