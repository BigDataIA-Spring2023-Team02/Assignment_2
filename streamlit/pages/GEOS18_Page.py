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
    st.image(Image.open('../Images/Satellite-data-for-imagery.jpeg'))
    
    BASE_URL = "http://localhost:8000"
    option = st.selectbox('Select the option to search file', ('Select Search Type', 'Search By Field 🔎', 'Search By Filename 🔎'))
    
    if option == 'Select Search Type':
        st.error('Select an input field')
    
    elif option == 'Search By Field 🔎':
        with st.spinner('Wait for it...'):
            st.markdown("<h3 style='text-align: center;'>Search Through Fields 🔎</h1>", unsafe_allow_html=True)
            response = requests.request("GET", f"{BASE_URL}/database/goes18")
            if response.status_code == 200:
                json_data = json.loads(response.text)
                products = json_data
            else:
                st.error("Database not populated.")
                st.stop()
            
            product_input = st.selectbox("Product name: ", products, disabled = True, key="selected_product")
            with st.spinner('Loading...'):
                response = requests.request("GET", f"{BASE_URL}/database/goes18/prod?product={product_input}")
            if response.status_code == 200:
                json_data = json.loads(response.text)
                years = json_data
            else:
                st.error("Incorrect input given, please change")
            
            year_input = st.selectbox("Year for which you are looking to get data for: ", [" "] + years, key="selected_year")
            if (year_input == " "):
                st.warning("Please select a year!")
            else:
                with st.spinner('Loading...'):
                    response = requests.request("GET", f"{BASE_URL}/database/goes18/prod/year?year={year_input}&product={product_input}")
                if response.status_code == 200:
                    json_data = json.loads(response.text)
                    days = json_data
                else:
                    st.error("Incorrect input given, please change")

                day_input = st.selectbox("Day within year for which you want data: ", [" "] + days, key="selected_day")
                if (day_input == " "):
                    st.warning("Please select a day!")
                else:
                    with st.spinner('Loading...'):
                        response = requests.request("GET", f"{BASE_URL}/database/goes18/prod/year/day?day={day_input}&year={year_input}&product={product_input}")
                    if response.status_code == 200:
                        json_data = json.loads(response.text)
                        hours = json_data
                    else:
                        st.error("Incorrect input given, please change")
                    
                    hour_input = st.selectbox("Hour of the day for which you want data: ", [" "] + hours, key='selected_hour')
                    if (hour_input == " "):
                        st.warning("Please select an hour!")
                    else:
                        with st.spinner("Loading..."):
                            response = requests.request("GET", f"{BASE_URL}/s3/goes18?year={year_input}&day={day_input}&hour={hour_input}&product={product_input}")
                        if response.status_code == 200:
                            json_data = json.loads(response.text)
                            files_available = json_data
                        else:
                            st.error("Incorrect input given, please change")

                        file_input = st.selectbox("Select a file: ", files_available, key='selected_file')
                        if st.button('Fetch file ©️'):
                            with st.spinner("Loading..."):
                                response = requests.request("POST", f"{BASE_URL}/s3/goes18/copyfile?file_name={file_input}&product={product_input}&year={year_input}&day={day_input}&hour={hour_input}")
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
            file_name = st.text_input('NOAA GEOS-18 Filename',)
            if st.button('Fetch file ©️'):
                with st.spinner("Loading..."):
                    response = requests.request("POST", f"{BASE_URL}/fetchfile/goes18?file_name={file_name}")
                if response.status_code == 404:
                    st.warning("No such file exists at GOES18 location")
                elif response.status_code == 400:
                    st.error("Invalid filename format for GOES18")
                else:
                    json_data = json.loads(response.text)
                    final_url = json_data
                    st.success("Found URL of the file available on GOES bucket!")
                    st.write("URL to file: ", final_url)

else:
    st.title("Please sign-in to access this feature!")