# Financial Analyzer Project

## Overview

The Financial Analyzer Project is a web application for analyzing and understanding spending behavior. Users can upload transaction data, perform detailed analyses, and compare different analyses over time.

## Features

- **Upload Transactions:** Upload transaction data via CSV files or single transactions.
- **Analyze Transactions:** Get a detailed analysis of spending and earning behavior.
- **Compare Analyses:** Compare the last three analyses to identify trends.

## Directory Structure
```
financial_analyzer_python/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── data_processing.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── financial_analyzer.py
│   │   ├── transaction_service.py
│   │   ├── interpretation.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── mongo.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── prompts.py
│   ├── data/
│   │   ├── plaid_transactions.csv
├── .env
├── .gitignore
├── requirements.txt
├── approaches.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Installation

### Prerequisites

- Python (Used Python-3.10.5 for dev)
- FastAPI 
- MongoDB

### Setup

1. Clone the repository and install dependencies:
```
git clone https://github.com/Aukerul-Shuvo/financial_analyzer_python.git
cd financial_analyzer_python
pip install -r requirements.txt
```

2. Create a .env file with the following variables:
```
MONGO_URI=<YOUR DB URI>
DATABASE_NAME=<YOUR DB NAME>
```

3. Run the application:
```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
``` 

4. Swagger UI:
```
`http://127.0.0.1:8000/docs`
```

### Running with Docker
Build and run the Docker container:
```
docker-compose up --build
```
