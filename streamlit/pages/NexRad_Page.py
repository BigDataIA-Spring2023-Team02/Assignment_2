import json
import requests
import streamlit as st
from PIL import Image

if 'username' not in st.session_state:
    st.session_state.username = ''

if 'logout_disabled' not in st.session_state:
    st.session_state.logout_disabled = True

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

with st.sidebar:
    user = "Not Logged In" if st.session_state.username == "" else st.session_state.username
    st.write(f'Current User: {user}')
    logout_button = st.button('LogOut', disabled=st.session_state.logout_disabled)
    if logout_button:
        for key in st.session_state.keys():
            if key == 'login_disabled' or key == 'logout_disabled' or key == 'register_disabled':
                st.session_state[key] = not st.session_state[key]
            else:
                st.session_state[key] = ''
        st.session_state.login_disabled = False
        st.session_state.register_disabled = False
        st.experimental_rerun()

if not st.session_state.username == "" and "access_token" in st.experimental_get_query_params():
    st.markdown("<h2 style='text-align: center;'>Data Exploration of the GEOS dataset 🌎</h1>", unsafe_allow_html=True)
    st.header("")
    st.image(Image.open('../Images/SatelliteImage.jpeg'))
    
    BASE_URL = "http://localhost:8000"
    option = st.selectbox('Select the option to search file', ('Select Search Type', 'Search By Field 🔎', 'Search By Filename 🔎'))
    
    if option == 'Select Search Type':
        st.error('Select an input field')
    
    elif option == 'Search By Field 🔎':
        with st.spinner('Wait for it...'):
            st.markdown("<h3 style='text-align: center;'>Search Through Fields 🔎</h1>", unsafe_allow_html=True)
            response = requests.get(f"{BASE_URL}/noaa-database/nexrad")
            if response.status_code == 200:
                json_data = json.loads(response.text)
                years = json_data
            else:
                st.error("Database not populated.")
                st.stop()
            
            year_input = st.selectbox("Year for which you are looking to get data for: ", [" "] + years, key="selected_year")
            if (year_input == " "):
                st.warning("Please select a year!")
            else:
                with st.spinner("Loading..."):
                    response = requests.get(f"{BASE_URL}/noaa-database/nexrad/year?year={year_input}")
                if response.status_code == 200:
                    json_data = json.loads(response.text)
                    months = json_data
                else:
                    st.error("Incorrect input given, please change")
                
                month_input = st.selectbox("Month for which you are looking to get data for: ", [" "] + months, key="selected_month")
                if (month_input == " "):
                    st.warning("Please select month!")
                else:
                    with st.spinner("Loading..."):
                        response = requests.get(f"{BASE_URL}/noaa-database/nexrad/year/month?month={month_input}&year={year_input}")
                    if response.status_code == 200:
                        json_data = json.loads(response.text)
                        days = json_data
                    else:
                        st.error("Incorrect input given, please change")
                    
                    day_input = st.selectbox("Day within year for which you want data: ", [" "] + days, key="selected_day")
                    if (day_input == " "):
                        st.warning("Please select day!")
                    else:
                        with st.spinner("Loading..."):
                            response = requests.get(f"{BASE_URL}/noaa-database/nexrad/year/month/day?day={day_input}&month={month_input}&year={year_input}")
                        if response.status_code == 200:
                            json_data = json.loads(response.text)
                            station_codes = json_data
                        else:
                            st.error("Incorrect input given, please change")
                        
                        station_code_input = st.selectbox("Station for which you want data: ", [" "] + station_codes, key='selected_ground_station')
                        if (station_code_input == " "):
                            st.warning("Please select station code!")
                        else:
                            with st.spinner("Loading..."):
                                response = requests.get(f"{BASE_URL}/aws-s3/nexrad?year={year_input}&month={month_input}&day={day_input}&ground_station={station_code_input}")
                            if response.status_code == 200:
                                json_data = json.loads(response.text)
                                files_available_in_station_code = json_data
                            else:
                                st.error("Incorrect input given, please change")

                            file_input = st.selectbox("Select a file: ", files_available_in_station_code, key='selected_file')
                            if st.button('Fetch file ©️'):
                                with st.spinner("Loading..."):
                                    response = requests.post(f"{BASE_URL}/aws-s3/nexrad/copyfile?file_name={file_input}&year={year_input}&month={month_input}&day={day_input}&ground_station={station_code_input}")
                                if response.status_code == 200:
                                    json_data = json.loads(response.text)
                                    download_url = json_data
                                    st.success("File available for download.")
                                    st.write("URL to download file:", download_url)
                                else:
                                    st.error("Incorrect input given, please change")

    elif option == 'Search By Filename 🔎':
        with st.spinner('Wait for it...'):
            st.markdown("<h3 style='text-align: center;'>Search Through Filename 🔎</h1>", unsafe_allow_html=True)
            file_name = st.text_input('NOAA NexRad Filename',)
            if st.button('Fetch file ©️'):
                with st.spinner("Loading..."):
                    response = requests.post(f"{BASE_URL}/aws-s3-fetchfile/nexrad?file_name={file_name}")
                if response.status_code == 404:
                    st.warning("No such file exists at NEXRAD location")
                elif response.status_code == 400:
                    st.error("Invalid filename format for NexRad")
                else:
                    json_data = json.loads(response.text)
                    final_url = json_data
                    st.success("Found URL of the file available on NexRad bucket!")
                    st.write("URL to file: ", final_url)

else:
    st.title("Please sign-in to access this feature!")