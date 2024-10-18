
# UFC Data Pipeline with AWS S3 and Lambda

This repository contains a data pipeline project that processes and cleans UFC fight data stored in CSV format, using **AWS S3** and **AWS Lambda**. The pipeline automatically ingests raw data, processes it (data cleaning), and stores the cleaned version back to S3, making it ready for analysis.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [How It Works](#how-it-works)
- [Future Enhancements](#future-enhancements)

---

## Project Overview

The goal of this project is to automate the process of data ingestion, cleaning, and storage for UFC fight statistics. The pipeline is triggered by uploading a CSV file to an S3 bucket, processed by an AWS Lambda function that performs data cleaning, and then saves the cleaned data back into S3.

### Key Features:
- **AWS S3**: Used for storing raw and cleaned data.
- **AWS Lambda**: Serverless function that processes and cleans the data.
- **Automation**: The process is fully automated using S3 triggers and serverless compute via Lambda.

---

## Architecture

```
ufc-master-data/
└── ufc-data/
    ├── raw/      # Contains the raw data files (e.g., ufc-master-raw.csv)
    └── cleaned/  # Contains the cleaned and processed data files (e.g., ufc-master-cleaned.csv)
```

### Workflow:
1. **Raw Data Upload**: Raw UFC data (CSV) is uploaded to the `raw` folder in the S3 bucket (`ufc-master-data/ufc-data/raw/`).
2. **Processing with Lambda**: An AWS Lambda function is triggered to retrieve the raw data from S3, process it using **pandas** (a Python library), and clean the data.
3. **Store Cleaned Data**: The cleaned data is saved back into the `cleaned` folder in S3 (`ufc-master-data/ufc-data/cleaned/`).

---

## Technologies Used

- **AWS S3**: Used for storing both raw and cleaned data.
- **AWS Lambda**: Used for serverless data processing.
- **Python (pandas)**: Used for data manipulation and cleaning.
- **boto3**: Python SDK to interact with AWS services.

---

## Setup Instructions

### Prerequisites:
1. **AWS Account**: You'll need an AWS account to create an S3 bucket and Lambda functions.
2. **AWS CLI**: Make sure you have AWS CLI installed and configured with appropriate IAM roles.
3. **Python**: The Lambda function uses Python 3.x and requires `boto3` and `pandas`.

### Step 1: Create an S3 Bucket
- Log in to your AWS console and create a new S3 bucket named `ufc-master-data`.
- Inside the bucket, create two folders:
  - `ufc-data/raw/`
  - `ufc-data/cleaned/`

### Step 2: Deploy the Lambda Function
1. Create an AWS Lambda function using Python.
2. Upload the Python script (`lambda_function.py`) from this repository to the Lambda console.
3. Grant the Lambda function permissions to read from and write to the S3 bucket (`ufc-master-data`).

### Step 3: Configure S3 Trigger
- Set up an S3 trigger in the AWS console to invoke the Lambda function when a file is uploaded to the `ufc-data/raw/` folder.

---

## How It Works

1. **Uploading Raw Data**:
   - Raw data (e.g., `ufc-master-raw.csv`) is uploaded to `s3://ufc-master-data/ufc-data/raw/`.
   - This upload triggers the Lambda function.

2. **Processing and Cleaning**:
   - The Lambda function retrieves the CSV file from the `raw` folder, reads it into a **pandas DataFrame**, and performs basic cleaning operations:
     - Removing rows with missing values.
     - Removing duplicate rows.
   - You can extend the cleaning logic as needed.

3. **Storing Cleaned Data**:
   - After cleaning, the Lambda function writes the cleaned CSV back into S3 at `s3://ufc-master-data/ufc-data/cleaned/ufc-master-cleaned.csv`.

---

## Future Enhancements

- **Advanced Data Cleaning**: Add more sophisticated data transformation or validation steps.
- **Error Handling**: Improve error handling, logging, and alerting for failed pipeline runs.
- **Analytics**: Integrate with AWS Glue or Athena for querying the cleaned data directly from S3.
- **Monitoring**: Add AWS CloudWatch monitoring for the Lambda function to keep track of execution and failures.

---

## License
This project is open-sourced under the MIT License.

---

Feel free to reach out if you have any questions or suggestions for improvements!
