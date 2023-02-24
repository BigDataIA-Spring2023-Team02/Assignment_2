import os
import sqlite3

user_bucket = os.environ.get('USER_BUCKET_NAME')
dir_path = os.path.dirname(os.path.realpath(__file__))

if (os.environ.get('CI_FLAG')=='True'):
    pass    #to allow testing CI via github actions, set the variable through github
# else:   #else download the file stored by the airflow dag from the s3 bucket 
#     s3client.download_file(user_bucket, 'database-files/sql_scraped_database.db', f"{dir_path}/sql_scraped_database.db")

async def get_database_file():
    database_connection = sqlite3.connect('sql_scraped_database.db')    #connect to metadata db
    return database_connection