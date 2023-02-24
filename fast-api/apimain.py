from fastapi import FastAPI
from dotenv import load_dotenv
from router import noaa_database, aws_s3_files, s3_fetch_file

load_dotenv()

app = FastAPI()

app.include_router(noaa_database.router)
app.include_router(aws_s3_files.router)
app.include_router(s3_fetch_file.router)