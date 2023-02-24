import os
import sqlite3

user_bucket = os.environ.get('USER_BUCKET_NAME')
dir_path = os.path.dirname(os.path.realpath(__file__))

# if (os.environ.get('CI_FLAG')=='True'):
#     pass

async def get_database_file():
    database_connection = sqlite3.connect('airflow_scrape_data.db')
    return database_connection