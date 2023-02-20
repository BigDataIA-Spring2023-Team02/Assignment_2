import os
import time
import boto3
import folium
import sqlite3
import numpy as np
import streamlit as st
from PIL import Image
from streamlit_folium import st_folium
from streamlit_folium import folium_static

from fileurl_main import *
from aws_main import *
from scrape_metadata import *
from sqlite_main import *
from streamlit_test import *

load_dotenv()
clientLogs = boto3.client('logs',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_LOGS_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_LOGS_SECRET_KEY')
                        )

def write_logs(message: str):
    clientLogs.put_log_events(
        logGroupName = "Assignment02-logs",
        logStreamName = "Streamlit-Logs",
        logEvents = [
            {
                'timestamp' : int(time.time() * 1e3),
                'message' : message
            }
        ]
    )

aws_main = AWS_Main()

database_file_name = 'scrape_data.db'
database_file_path = os.path.join(os.path.dirname(__file__), database_file_name)
db = sqlite3.connect(database_file_path)

geos_data = pd.read_sql_query("SELECT * FROM GEOS18", db)
nexrad_data = pd.read_sql_query("SELECT * FROM NEXRAD", db)
nexradmap_data = pd.read_sql_query("SELECT * FROM NexradMap", db)

def geos_search_field(satellite_input):
    st.markdown("<h3 style='text-align: center;'>Search Through Fields 🔎</h1>", unsafe_allow_html=True)
    write_logs(f"GEOS Data by Search Field Inputs")
    
    with st.spinner('Wait for it...'):
        products = geos_data['Product_Name'].unique()
        products = np.insert(products, 0, "")
        product_input = st.selectbox('Select Product Name', products)
        if product_input:
            years = geos_data[geos_data['Product_Name'] == product_input]['Year'].unique()
            years = np.insert(years, 0, "")
            year_input = st.selectbox('Select Year', years)
            if year_input:
                day = geos_data[geos_data['Year'] == year_input]['Day'].unique()
                day = np.insert(day, 0, "")
                day_input = st.selectbox('Select Day', day)
                if day_input:
                    hour = geos_data[geos_data['Day'] == day_input]['Hour'].unique()
                    hour = np.insert(hour, 0, "")
                    hour_input = st.selectbox('Select Hour', hour)
                    if hour_input:
                        with st.spinner('Wait for it...'):
                            files_list = aws_main.list_files_in_noaa_goes18_bucket(product_input, year_input, day_input, hour_input)
                            files_list = np.insert(files_list, 0, "")
                            file_input = st.selectbox('Select File Name', files_list)
                            write_logs(f"Selected file to copy to user bucket {file_input}")
                            
                            if st.button('Copy to User S3 Bucket ©️'):
                                selected_file = product_input + '/' + year_input + '/' + day_input + '/' + hour_input + '/' + file_input
                                write_logs(f"Selected file key: {selected_file}")
                                with st.spinner('Wait for it...'):
                                    url_s3, url_noaa = aws_main.copy_file_to_user_bucket(selected_file, file_input, satellite_input)
                                    write_logs(f"Returning file link available in user bucket for selected file{file_input}: {url_s3}")
                                    write_logs(f"Returning file link from NOAA bucket for selected file {file_input}: {url_noaa}")

def geos_search_filename(satellite_input):
    st.markdown("<h3 style='text-align: center;'>Search Through Filename 🔎</h1>", unsafe_allow_html=True)
    write_logs(f"GEOS Data by Search Filename Inputs")
    with st.spinner('Wait for it...'):
        file_name = st.text_input('NOAA GEOS-18 Filename',)
        try:
            if st.button('Copy to User S3 Bucket ©️'):
                with st.spinner('Wait for it...'):
                    url, selected_file_key = goes_18_link_generation(file_name)
                    url_s3, url_noaa = aws_main.copy_file_to_user_bucket(selected_file_key, file_name, satellite_input)
                    write_logs(f"Returning file link available in user bucket for selected file{file_name}: {url_s3}")
                    write_logs(f"Returning file link from NOAA bucket for selected file {file_name}: {url_noaa}")
                
        except ValueError:
            write_logs(f"Not able to generate filename URL")
            st.error('Oops! Unable to Generate')

def nexrad_search_field(satellite_input):
    st.markdown("<h3 style='text-align: center;'>Search Through Fields 🔎</h1>", unsafe_allow_html=True)
    write_logs(f"NexRad Data by Search Field Inputs")
    
    with st.spinner('Wait for it...'):
        years = nexrad_data['Year'].unique()
        years = np.insert(years, 0, "")
        year_input = st.selectbox('Select Year', years)
        if year_input:
            months = nexrad_data[nexrad_data['Year'] == year_input]['Month'].unique()
            months = np.insert(months, 0, "")
            month_input = st.selectbox('Select Month', months)
            if month_input:
                day = nexrad_data[nexrad_data['Month'] == month_input]['Day'].unique()
                day = np.insert(day, 0, "")
                day_input = st.selectbox('Select Day', day)
                if day_input:
                    station_code = nexrad_data[nexrad_data['Day'] == day_input]['NexRad Station Code'].unique()
                    station_code = np.insert(station_code, 0, "")
                    station_code_input = st.selectbox('NexRad Station Code', station_code)
                    if station_code_input:
                        with st.spinner('Wait for it...'):
                            files_list = aws_main.list_files_in_noaa_nexrad_bucket(year_input, month_input, day_input, station_code_input)
                            files_list = np.insert(files_list, 0, "")
                            file_input = st.selectbox('Select File Name',files_list)
                            write_logs(f"Selected file to copy to user bucket {file_input}")
                            
                            if st.button('Copy to User S3 Bucket ©️'):
                                selected_file = year_input + '/' + month_input + '/' + day_input + '/' + station_code_input + '/' + file_input
                                write_logs(f"Selected file key: {selected_file}")
                                with st.spinner('Wait for it...'):
                                    url_s3, url_noaa = aws_main.copy_file_to_user_bucket(selected_file, file_input, satellite_input)
                                    write_logs(f"Returning file link available in user bucket for selected file{file_input}: {url_s3}")
                                    write_logs(f"Returning file link from NOAA bucket for selected file {file_input}: {url_noaa}")

def nexrad_search_filename(satellite_input):
    st.markdown("<h3 style='text-align: center;'>Search Through Filename 🔎</h1>", unsafe_allow_html=True)
    write_logs(f"NexRad Data by Search Filename Inputs")
    with st.spinner('Wait for it...'):
        file_name = st.text_input('NOAA NexRad Filename',)
        try:
            if st.button('Copy to User S3 Bucket ©️'):
                with st.spinner('Wait for it...'):
                    url, selected_file_key = nexrad_link_generation(file_name)
                    url_s3, url_noaa = aws_main.copy_file_to_user_bucket(selected_file_key, file_name, satellite_input)
                    write_logs(f"Returning file link available in user bucket for selected file{file_name}: {url_s3}")
                    write_logs(f"Returning file link from NOAA bucket for selected file {file_name}: {url_noaa}")

        except ValueError:
            write_logs(f"Not able to generate filename URL")
            st.error('Oops! Unable to Generate')

def geos_dataset():
    with st.spinner('Wait for it...'):
        option = st.selectbox('Select the option to search file', ('--Select Search Type--', 'Search By Field 🔎', 'Search By Filename 🔎'))
        satellite_input = 'geos18'
        
        if option == '--Select Search Type--':
            st.error('Select an input field')
        
        elif option == 'Search By Field 🔎':
            with st.spinner('Wait for it...'):
                geos_search_field(satellite_input)
        
        elif option == 'Search By Filename 🔎':
            with st.spinner('Wait for it...'):
                geos_search_filename(satellite_input)

def nexrad_dataset():
    with st.spinner('Wait for it...'):
        option = st.selectbox('Select the option to search file', ('--Select Search Type--', 'Search By Field 🔎', 'Search By Filename 🔎'))
        satellite_input = 'nexrad'
        
        if option == '--Select Search Type--':
            st.error('Select an input field')
        
        elif option == 'Search By Field 🔎':
            with st.spinner('Wait for it...'):
                nexrad_search_field(satellite_input)
        
        elif option == 'Search By Filename 🔎':
            with st.spinner('Wait for it...'):
                nexrad_search_filename(satellite_input)

def nexrad_mapdata():
    write_logs(f"NEXRAD Map Data Exploration")
    st.map(nexradmap_data)
    
    m = folium.Map(location=[40,-100], tiles="OpenStreetMap", zoom_start=4)
    for i in range(0,len(nexradmap_data)):
        folium.Marker(
        location = [nexradmap_data.iloc[i]['latitude'], nexradmap_data.iloc[i]['longitude']],
        popup = (nexradmap_data.iloc[i]['Station_Code'],nexradmap_data.iloc[i]['County'])
        ).add_to(m)

    st.markdown("<h2 style='text-align: center;'>Nexrad Station Pointers</h1>", unsafe_allow_html=True)
    folium_static(m)


def noaa_dashboard():
    with st.sidebar:
        st.header('Select an option:')
        page = st.sidebar.selectbox("Choose a page", ["Home Page", "GEOS Data 🌎", "NexRad Data 🌎", "NexRad Map Locations 📍"])
        for i in range(15):
            st.write("")
        st.sidebar.image("Images/Earth-Free-Download-PNG.png", use_column_width = True,  width = 200)
    
    st.markdown("<h1 style='text-align: center;'>Geospatial Data Exploration Tool 🔭</h1>", unsafe_allow_html=True)
    
    if page == "Home Page":
        st.markdown("<h3 style='text-align: center;'>Select page from the Left Selectbox</h1>", unsafe_allow_html=True)
        st.write('')
        st.image(Image.open('Images/DataExploration.png'))
    
    elif page == "GEOS Data 🌎":
        st.markdown("<h2 style='text-align: center;'>Data Exploration of the GEOS dataset 🌎</h1>", unsafe_allow_html=True)
        st.write('')
        st.image(Image.open('Images/Satellite-data-for-imagery.jpeg'))
        write_logs(f"Running GEOS dataset file download script")
        geos_dataset()

    elif page == "NexRad Data 🌎":
        st.markdown("<h2 style='text-align: center;'>Data Exploration of the NexRad dataset 🌎</h1>", unsafe_allow_html=True)
        st.write('')
        st.image(Image.open('Images/SatelliteImage.jpeg'))
        write_logs(f"Running NEXRAD dataset file download script")
        nexrad_dataset()
    
    elif page == "NexRad Map Locations 📍":
        st.markdown("<h2 style='text-align: center;'>NexRad Map Geo-Locations 📍</h1>", unsafe_allow_html=True)
        write_logs(f"Running NEXRAD Map Geo-location script")
        nexrad_mapdata()

def main():
    noaa_dashboard()

if __name__ == "__main__":
    main()