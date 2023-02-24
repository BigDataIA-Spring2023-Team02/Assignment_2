import os
import boto3
import sqlite3
from dotenv import load_dotenv

#load env variables
load_dotenv()

s3client = boto3.client('s3',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')
                        )

async def get_database_file():
    database_connection = sqlite3.connect('airflow_scrape_data.db')
    return database_connection