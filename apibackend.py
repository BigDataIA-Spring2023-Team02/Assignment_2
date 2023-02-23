import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Table, MetaData, select


app = FastAPI()
engine=create_engine('sqlite:///scrape_data.db')


# Load the metadata file
scrapedata = MetaData(bind= engine)


scrapedata.reflect(engine)


# Define a Pydantic model to represent a row in the table GEOS18
class GEOS18(BaseModel):
   ID: int
   Product_Name: str
   Year: int
   Day: int
   Hour: int


# Define a Pydantic model to represent a row in the table NexRad
class NEXRAD(BaseModel):
   ID:int
   Year: int
   Month: int
   Day: int
   NexRad_Station_Code: str


# Define the geos18 table object using the metadata
geos18 = Table('GEOS18', scrapedata, autoload=True)
nexrad = Table('NEXRAD', scrapedata, autoload=True)
print(nexrad.columns)


# Define a function to query the database
def query_geos18(ID:int = None, Product_Name: str = None, Year: int = None, Day: int = None, Hour: int = None):
   # Build the SQL query based on the supplied query parameters
   query = select([geos18])
   print(query)
  
   if ID:
       query = query.where(geos18.columns.ID==ID)
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
   geos18_data = []
   for row in results:
       geos18_data.append({
           'Product_Name': row.Product_Name,
           'Year': row.Year,
           'Day': row.Day,
           'Hour': row.Hour
       })
  
   return geos18_data






def query_nexrad(ID: int = None, Year: int = None, Month: int = None, Day: int = None, NexRad_Station_Code: str = None):
   # Build the SQL query based on the supplied query parameters
   query = select([nexrad])
  
   if ID:
       query = query.where(nexrad.columns.ID == ID)
   if Year:
       query = query.where(nexrad.columns.Year == Year)
       if Month:
           query = query.where(nexrad.columns.Month == Month)
           if Day:
               query = query.where(nexrad.columns.Day == Day)
               if NexRad_Station_Code:
                   query = query.where(nexrad.columns.NexRad_Station_Code == NexRad_Station_Code)
   elif Month:
       query = query.where(nexrad.columns.Month == Month)
       if Day:
           query = query.where(nexrad.columns.Day == Day)
           if NexRad_Station_Code:
               query = query.where(nexrad.columns.NexRad_Station_Code == NexRad_Station_Code)
   elif Day:
       query = query.where(nexrad.columns.Day == Day)
       if NexRad_Station_Code:
           query = query.where(nexrad.columns.NexRad_Station_Code == NexRad_Station_Code)
   elif NexRad_Station_Code:
       query = query.where(nexrad.columns.NexRad_Station_Code == NexRad_Station_Code)


   # Execute the query and fetch the results
   results = query.execute().fetchall()


   # Convert the results to a list of dictionaries
   nexrad_data = []
   for row in results:
       nexrad_data.append({
           'Year': row.Year,
           'Month': row.Month,
           'Day': row.Day,
           'NexRad_Station_Code': row.NexRad_Station_Code
       })
   print(nexrad.columns)
  
   return nexrad_data




# Define a GET endpoint to retrieve data from the geos18 table
@app.get('/GEOS18')
async def get_geos18(Product_Name: str = None, Year: int = None, Day: int = None, Hour: int = None):
   geos18_data = query_geos18(Product_Name=Product_Name, Year=Year, Day=Day, Hour=Hour)
  
   return JSONResponse(content=geos18_data)




# Define a GET endpoint to retrieve data from the nexrad table
@app.get('/NEXRAD')
async def get_nexrad(Year: int = None, Month: int = None, Day: int = None, NexRad_Station_Code: str = None):
   nexrad_data = query_nexrad(Year=Year, Month=Month, Day=Day, NexRad_Station_Code=NexRad_Station_Code)
  
   return JSONResponse(content=nexrad_data)