import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Table, MetaData, select

app = FastAPI()

# Load the metadata file
scrapedata = MetaData()
scrapedata.reflect(bind=create_engine('sqlite:///scrape_data.db'))

# Define a Pydantic model to represent a row in the table GEOS18
class GEOS18(BaseModel):
    Product_Name: str
    Year: int
    Day: int
    Hour: int

# Define a Pydantic model to represent a row in the table NexRad
class NEXRAD(BaseModel):
    Year: str
    Month: int
    Day: int
    NexRad_Station_Code: int

# Define the geos18 table object using the metadata
geos18 = Table('GEOS18', scrapedata, autoload=True)
nexrad = Table('NEXRAD', scrapedata, autoload=True)

# Define a function to query the database
def query_geos18(Product_Name: str = None, Year: int = None, Day: int = None, Hour: int = None):
    # Build the SQL query based on the supplied query parameters
    query = select([geos18])
    if Product_Name:
        query = query.where(geos18.columns.Product_Name == Product_Name)
        if Year:
            query = query.where(geos18.columns.Year == Year)
            if Day:
                query = query.where(geos18.columns.Day == Day)
                if Hour:
                    query = query.where(geos18.columns.Hour == Hour)
        elif Day:
            query = query.where(geos18.columns.Day == Day)
            if Hour:
                query = query.where(geos18.columns.Hour == Hour)
        elif Hour:
            query = query.where(geos18.columns.Hour == Hour)

    # Execute the query and fetch the results
    results = query.execute().fetchall()

    # Convert the results to a list of dictionaries
    data = []
    for row in results:
        data.append({
            'Product_Name': row.Product_Name,
            'Year': row.Year,
            'Day': row.Day,
            'Hour': row.Hour
        })
    
    return data

# Define a GET endpoint to retrieve data from the geos18 table
@app.get('/GEOS18')
async def get_geos18(Product_Name: str = None, Year: int = None, Day: int = None, Hour: int = None):
    data = query_geos18(Product_Name=Product_Name, Year=Year, Day=Day, Hour=Hour)
    return JSONResponse(content=data)
