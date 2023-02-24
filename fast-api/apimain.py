from noaa_database import noaa_database
from aws_s3_files import aws_s3_files
from s3_fetch_file import s3_fetch_file
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(noaa_database.router)
app.include_router(aws_s3_files.router)
app.include_router(s3_fetch_file.router)