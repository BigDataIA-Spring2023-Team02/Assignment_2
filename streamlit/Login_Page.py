import json
import os
import boto3
import requests
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from requests.exceptions import HTTPError
from fastapi.security import OAuth2PasswordBearer
from streamlit_extras.switch_page_button import switch_page
import folium
import streamlit_folium as stf

#load env variables
load_dotenv()

API_URL = "http://localhost:8000"

#authenticate S3 client for logging with your user credentials that are stored in your .env config file
clientLogs = boto3.client('logs',
                        region_name='us-east-1',
                        aws_access_key_id = os.environ.get('AWS_LOG_ACCESS_KEY'),
                        aws_secret_access_key = os.environ.get('AWS_LOG_SECRET_KEY')
                        )

if 'username' not in st.session_state:
    st.session_state.username = ''

if 'password' not in st.session_state:
    st.session_state.password = ''

if 'access_token' not in st.session_state:
    st.session_state.access_token = ''

if 'login_disabled' not in st.session_state:
    st.session_state.login_disabled = False

if 'logout_disabled' not in st.session_state:
    st.session_state.logout_disabled = True

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# if 'logged_in' not in st.session_state:
#     st.session_state['logged_in'] = False
#     st.session_state['access_token'] = ''
#     st.session_state['username'] = ''

# if st.session_state['logged_in'] == True:
#     col1, col2, col3 , col4, col5 = st.columns(5)

#     with col1:
#         pass
#     with col2:
#         pass
#     with col3 :
#         pass
#     with col4:
#         pass
#     with col5:
#         logout_button = st.button(label='Logout', disabled=False)

#     if logout_button:
#         st.session_state['logged_in'] = False
#         st.experimental_rerun()

# def geos18():
#     if 'username' not in st.session_state:
#         st.session_state.username = ''

#     if 'logout_disabled' not in st.session_state:
#         st.session_state.logout_disabled = True

#     if 'logged_in' not in st.session_state:
#         st.session_state.logged_in = False

#     with st.sidebar:
#         user = "Not Logged In" if st.session_state.username == "" else st.session_state.username
#         st.write(f'Current User: {user}')
#         logout_button = st.button('LogOut', disabled=st.session_state.logout_disabled)
#         if logout_button:
#             for key in st.session_state.keys():
#                 if key == 'login_disabled' or key == 'logout_disabled' or key == 'register_disabled':
#                     st.session_state[key] = not st.session_state[key]
#                 else:
#                     st.session_state[key] = ''
#             st.session_state.login_disabled = False
#             st.session_state.register_disabled = False
#             st.experimental_rerun()

#     if not st.session_state.username == "" and "access_token" in st.experimental_get_query_params():
#         st.markdown("<h2 style='text-align: center;'>Data Exploration of the GEOS dataset 🌎</h1>", unsafe_allow_html=True)
#         st.header("")
#         st.image(Image.open('../Images/Satellite-data-for-imagery.jpeg'))
        
#         BASE_URL = "http://localhost:8000"
#         option = st.selectbox('Select the option to search file', ('Select Search Type', 'Search By Field 🔎', 'Search By Filename 🔎'))
        
#         if option == 'Select Search Type':
#             st.error('Select an input field')
        
#         elif option == 'Search By Field 🔎':
#             with st.spinner('Wait for it...'):
#                 st.markdown("<h3 style='text-align: center;'>Search Through Fields 🔎</h1>", unsafe_allow_html=True)
#                 response = requests.get(f"{BASE_URL}/noaa-database/goes18")
#                 if response.status_code == 200:
#                     json_data = json.loads(response.text)
#                     products = json_data
#                 else:
#                     st.error("Database not populated.")
#                     st.stop()
                
#                 product_input = st.selectbox("Product name: ", products, disabled = True, key="selected_product")
#                 with st.spinner('Loading...'):
#                     response = requests.get(f"{BASE_URL}/noaa-database/goes18/prod?product={product_input}")
#                 if response.status_code == 200:
#                     json_data = json.loads(response.text)
#                     years = json_data
#                 else:
#                     st.error("Incorrect input given, please change")
                
#                 year_input = st.selectbox("Year for which you are looking to get data for: ", [" "] + years, key="selected_year")
#                 if (year_input == " "):
#                     st.warning("Please select a year!")
#                 else:
#                     with st.spinner('Loading...'):
#                         response = requests.get(f"{BASE_URL}/noaa-database/goes18/prod/year?year={year_input}&product={product_input}")
#                     if response.status_code == 200:
#                         json_data = json.loads(response.text)
#                         days = json_data
#                     else:
#                         st.error("Incorrect input given, please change")

#                     day_input = st.selectbox("Day within year for which you want data: ", [" "] + days, key="selected_day")
#                     if (day_input == " "):
#                         st.warning("Please select a day!")
#                     else:
#                         with st.spinner('Loading...'):
#                             response = requests.get(f"{BASE_URL}/noaa-database/goes18/prod/year/day?day={day_input}&year={year_input}&product={product_input}")
#                         if response.status_code == 200:
#                             json_data = json.loads(response.text)
#                             hours = json_data
#                         else:
#                             st.error("Incorrect input given, please change")
                        
#                         hour_input = st.selectbox("Hour of the day for which you want data: ", [" "] + hours, key='selected_hour')
#                         if (hour_input == " "):
#                             st.warning("Please select an hour!")
#                         else:
#                             with st.spinner("Loading..."):
#                                 response = requests.get(f"{BASE_URL}/aws-s3/goes18?year={year_input}&day={day_input}&hour={hour_input}&product={product_input}")
#                             if response.status_code == 200:
#                                 json_data = json.loads(response.text)
#                                 files_available = json_data
#                             else:
#                                 st.error("Incorrect input given, please change")

#                             file_input = st.selectbox("Select a file: ", files_available, key='selected_file')
#                             if st.button('Fetch file ©️'):
#                                 with st.spinner("Loading..."):
#                                     response = requests.post(f"{BASE_URL}/aws-s3/goes18/copyfile?file_name={file_input}&product={product_input}&year={year_input}&day={day_input}&hour={hour_input}")
#                                 if response.status_code == 200:
#                                     json_data = json.loads(response.text)
#                                     download_url = json_data
#                                     st.success("File available for download.")
#                                     st.write("URL to download file:", download_url)
#                                 else:
#                                     st.error("Incorrect input given, please change")
        
#         elif option == 'Search By Filename 🔎':
#             with st.spinner('Wait for it...'):
#                 st.markdown("<h3 style='text-align: center;'>Search Through Filename 🔎</h1>", unsafe_allow_html=True)
#                 file_name = st.text_input('NOAA GEOS-18 Filename',)
#                 if st.button('Fetch file ©️'):
#                     with st.spinner("Loading..."):
#                         response = requests.post(f"{BASE_URL}/aws-s3-fetchfile/goes18?file_name={file_name}")
#                     if response.status_code == 404:
#                         st.warning("No such file exists at GOES18 location")
#                     elif response.status_code == 400:
#                         st.error("Invalid filename format for GOES18")
#                     else:
#                         json_data = json.loads(response.text)
#                         final_url = json_data
#                         st.success("Found URL of the file available on GOES bucket!")
#                         st.write("URL to file: ", final_url)

#     else:
#         st.title("Please sign-in to access this feature!")

# def nexrad():
#     if 'username' not in st.session_state:
#         st.session_state.username = ''

#     if 'logout_disabled' not in st.session_state:
#         st.session_state.logout_disabled = True

#     if 'logged_in' not in st.session_state:
#         st.session_state.logged_in = False

#     with st.sidebar:
#         user = "Not Logged In" if st.session_state.username == "" else st.session_state.username
#         st.write(f'Current User: {user}')
#         logout_button = st.button('LogOut', disabled=st.session_state.logout_disabled)
#         if logout_button:
#             for key in st.session_state.keys():
#                 if key == 'login_disabled' or key == 'logout_disabled' or key == 'register_disabled':
#                     st.session_state[key] = not st.session_state[key]
#                 else:
#                     st.session_state[key] = ''
#             st.session_state.login_disabled = False
#             st.session_state.register_disabled = False
#             st.experimental_rerun()

#     if not st.session_state.username == "" and "access_token" in st.experimental_get_query_params():
#         st.markdown("<h2 style='text-align: center;'>Data Exploration of the GEOS dataset 🌎</h1>", unsafe_allow_html=True)
#         st.header("")
#         st.image(Image.open('../Images/SatelliteImage.jpeg'))
        
#         BASE_URL = "http://localhost:8000"
#         option = st.selectbox('Select the option to search file', ('Select Search Type', 'Search By Field 🔎', 'Search By Filename 🔎'))
        
#         if option == 'Select Search Type':
#             st.error('Select an input field')
        
#         elif option == 'Search By Field 🔎':
#             with st.spinner('Wait for it...'):
#                 st.markdown("<h3 style='text-align: center;'>Search Through Fields 🔎</h1>", unsafe_allow_html=True)
#                 response = requests.get(f"{BASE_URL}/noaa-database/nexrad")
#                 if response.status_code == 200:
#                     json_data = json.loads(response.text)
#                     years = json_data
#                 else:
#                     st.error("Database not populated.")
#                     st.stop()
                
#                 year_input = st.selectbox("Year for which you are looking to get data for: ", [" "] + years, key="selected_year")
#                 if (year_input == " "):
#                     st.warning("Please select a year!")
#                 else:
#                     with st.spinner("Loading..."):
#                         response = requests.get(f"{BASE_URL}/noaa-database/nexrad/year?year={year_input}")
#                     if response.status_code == 200:
#                         json_data = json.loads(response.text)
#                         months = json_data
#                     else:
#                         st.error("Incorrect input given, please change")
                    
#                     month_input = st.selectbox("Month for which you are looking to get data for: ", [" "] + months, key="selected_month")
#                     if (month_input == " "):
#                         st.warning("Please select month!")
#                     else:
#                         with st.spinner("Loading..."):
#                             response = requests.get(f"{BASE_URL}/noaa-database/nexrad/year/month?month={month_input}&year={year_input}")
#                         if response.status_code == 200:
#                             json_data = json.loads(response.text)
#                             days = json_data
#                         else:
#                             st.error("Incorrect input given, please change")
                        
#                         day_input = st.selectbox("Day within year for which you want data: ", [" "] + days, key="selected_day")
#                         if (day_input == " "):
#                             st.warning("Please select day!")
#                         else:
#                             with st.spinner("Loading..."):
#                                 response = requests.get(f"{BASE_URL}/noaa-database/nexrad/year/month/day?day={day_input}&month={month_input}&year={year_input}")
#                             if response.status_code == 200:
#                                 json_data = json.loads(response.text)
#                                 station_codes = json_data
#                             else:
#                                 st.error("Incorrect input given, please change")
                            
#                             station_code_input = st.selectbox("Station for which you want data: ", [" "] + station_codes, key='selected_ground_station')
#                             if (station_code_input == " "):
#                                 st.warning("Please select station code!")
#                             else:
#                                 with st.spinner("Loading..."):
#                                     response = requests.get(f"{BASE_URL}/aws-s3/nexrad?year={year_input}&month={month_input}&day={day_input}&ground_station={station_code_input}")
#                                 if response.status_code == 200:
#                                     json_data = json.loads(response.text)
#                                     files_available_in_station_code = json_data
#                                 else:
#                                     st.error("Incorrect input given, please change")

#                                 file_input = st.selectbox("Select a file: ", files_available_in_station_code, key='selected_file')
#                                 if st.button('Fetch file ©️'):
#                                     with st.spinner("Loading..."):
#                                         response = requests.post(f"{BASE_URL}/aws-s3/nexrad/copyfile?file_name={file_input}&year={year_input}&month={month_input}&day={day_input}&ground_station={station_code_input}")
#                                     if response.status_code == 200:
#                                         json_data = json.loads(response.text)
#                                         download_url = json_data
#                                         st.success("File available for download.")
#                                         st.write("URL to download file:", download_url)
#                                     else:
#                                         st.error("Incorrect input given, please change")

#         elif option == 'Search By Filename 🔎':
#             with st.spinner('Wait for it...'):
#                 st.markdown("<h3 style='text-align: center;'>Search Through Filename 🔎</h1>", unsafe_allow_html=True)
#                 file_name = st.text_input('NOAA NexRad Filename',)
#                 if st.button('Fetch file ©️'):
#                     with st.spinner("Loading..."):
#                         response = requests.post(f"{BASE_URL}/aws-s3-fetchfile/nexrad?file_name={file_name}")
#                     if response.status_code == 404:
#                         st.warning("No such file exists at NEXRAD location")
#                     elif response.status_code == 400:
#                         st.error("Invalid filename format for NexRad")
#                     else:
#                         json_data = json.loads(response.text)
#                         final_url = json_data
#                         st.success("Found URL of the file available on NexRad bucket!")
#                         st.write("URL to file: ", final_url)

#     else:
#         st.title("Please sign-in to access this feature!")

# def nexradmap():
#     if 'username' not in st.session_state:
#         st.session_state.username = ''

#     if 'logout_disabled' not in st.session_state:
#         st.session_state.logout_disabled = True

#     if 'logged_in' not in st.session_state:
#         st.session_state.logged_in = False

#     with st.sidebar:
#         user = "Not Logged In" if st.session_state.username == "" else st.session_state.username
#         st.write(f'Current User: {user}')
#         logout_button = st.button('LogOut', disabled=st.session_state.logout_disabled)
#         if logout_button:
#             for key in st.session_state.keys():
#                 if key == 'login_disabled' or key == 'logout_disabled' or key == 'register_disabled':
#                     st.session_state[key] = not st.session_state[key]
#                 else:
#                     st.session_state[key] = ''
#             st.session_state.login_disabled = False
#             st.session_state.register_disabled = False
#             st.experimental_rerun()

#     if not st.session_state.username == "" and "access_token" in st.experimental_get_query_params():
#         st.markdown("<h2 style='text-align: center;'>NexRad Map Geo-Locations 📍</h1>", unsafe_allow_html=True)
        
#         BASE_URL = "http://localhost:8000"
        
#         with st.spinner('Refreshing map locations ...'):
            
#             response = requests.get(f"{BASE_URL}/noaa-database/mapdata")#, headers=headers)
#             if response.status_code == 404:
#                 st.warning("Unable to fetch mapdata")
#                 st.stop()
#             else:
#                 json_data = json.loads(response.text)
#                 map_dict = json_data

#             map = folium.Map(location=[40,-100], tiles="OpenStreetMap", zoom_start=4)
#             for i in range(0,len(map_dict)):
#                 folium.Marker(
#                 location = [map_dict.iloc[i]['latitude'], map_dict.iloc[i]['longitude']],
#                 popup = (map_dict.iloc[i]['Station_Code'],map_dict.iloc[i]['County'])
#                 ).add_to(map)

#             st.markdown("<h2 style='text-align: center;'>Nexrad Station Pointers</h1>", unsafe_allow_html=True)
#             stf.st_folium(map, width=700, height=460)
            
#     else:
#         st.title("Please sign-in to access this feature!")

# if st.session_state['logged_in'] == False:
#     login_or_signup = st.selectbox("Please select an option", ["Login", "Signup"])

#     if login_or_signup=="Login":
#         st.write("Enter your credentials to login")
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
#         if st.button("Login"):
#             if username == '' or password == '':
#                 st.warning("Please enter both username and password.")
#             else:
#                 with st.spinner("Wait.."):
#                     payload = {'username': username, 'password': password}
#                     try:
#                         response = requests.request("POST", f"{API_URL}/login", data=payload)
                        
#                     except:
#                         st.error("Service unavailable, please try again later") #in case the API is not running
#                         st.stop()   #stop the application
#                 if response.status_code == 200:
#                     json_data = json.loads(response.text)
#                     st.session_state['if_logged'] = True
#                     st.session_state['access_token'] = json_data['access_token']
#                     st.session_state['username'] = username
#                     st.success("Login successful")
#                     st.experimental_rerun()
#                 else:
#                     st.error("Incorrect username or password.")

#     elif login_or_signup=="Signup":
#         st.write("Create an account to get started")
#         full_name = st.text_input("Full_Name")
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
#         confirm_password = st.text_input("Confirm Password", type="password")
#         if st.button("Signup"):
#             if len(password) < 4:
#                 st.warning("Password should be of 4 characters minimum")
#             elif full_name == '' or username == '' or password == '' or confirm_password == '':
#                 st.warning("Please fill in all the fields.")
#             elif password != confirm_password:
#                 with st.spinner("Wait.."):
#                     st.warning("Passwords do not match.")
#             else:
#                 with st.spinner("Wait.."):
#                     try:
#                         payload = {'full_name': full_name, 'username': username, 'password': password}
#                         response = requests.request("POST", f"{API_URL}/user/create", json=payload)
                        
#                     except:
#                         st.error("Service unavailable, please try again later") #in case the API is not running
#                         st.stop()   #stop the application
#                 if response.status_code == 200:
#                     st.success("Account created successfully! Please login to continue.")
#                 else:
#                     st.error("Error creating account. Please try again.")

# if st.session_state['logged_in'] == True:
#     page = st.sidebar.selectbox("Select a page", ["GOES-18", "NEXRAD", "NEXRAD Locations - Map"])   #main options of streamlit app

#     if page == "GOES-18":
#         with st.spinner("Loading..."): #spinner element
#             geos18()
#     elif page == "NEXRAD":
#         with st.spinner("Loading..."): #spinner element
#             nexrad()
#     elif page == "NEXRAD Locations - Map":
#         with st.spinner("Generating map..."): #spinner element
#             nexradmap()

def login():
    st.title("Login Page !!!")
    st.header("NOAA Data Exploration Tool !!!")
    st.subheader("Existing user? Login below.")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    
    username = st.text_input("Username", st.session_state.username, placeholder='Username')
    password = st.text_input("Password", st.session_state.password, placeholder='Password', type = 'password')
    login_button = st.button('Login', disabled = st.session_state.login_disabled)

    if "access_token" in st.experimental_get_query_params():
        headers = {
            "Authorization": f"Bearer {st.experimental_get_query_params()['access_token'][0]}"
        }
        url = "http://localhost:8000/users/{id}"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            user_info = response.json()
            st.session_state.username = user_info['username']
            st.session_state.disable_login=True

        except HTTPError:
            st.session_state.username = ''
            query_params = st.experimental_get_query_params()
            query_params["access_token"] = None
            st.experimental_set_query_params(**query_params)
        except Exception as error:
            st.error(f"Error: {error}")
        st.session_state.disable_logout = False
    
    if login_button:
        if username == "" or password == "":
            st.warning("Please enter both username and password.")
        else:
            st.session_state.username = username
            st.session_state.password = password
            user_log = {
                'username': st.session_state.username,
                'password': st.session_state.password
            }
            res = requests.post(url='http://localhost:8000/login', json=user_log)
            if res and res.status_code == 200:
                st.success("Logged in successfully as {}".format(username))
                st.session_state.access_token = res.json()['access_token']
                st.experimental_set_query_params(access_token=st.session_state.access_token)
                st.session_state.login_disabled = True
                st.session_state.logged_in = True
                st.session_state.logout_disabled = False
                switch_page('GEOS18_Page')

            elif res.status_code == 401:
                switch_page('Register_Page')
            else:
                st.error("Error: User doesn't exist!")

    with st.sidebar:
        if st.session_state and st.session_state.logged_in and st.session_state.username:
            st.write(f'Current User: {st.session_state.username}')
        else:
            st.write('Current User: Not Logged In')

        logout_button = st.button('Log Out', disabled = st.session_state.logout_disabled)
        if logout_button:
            for key in st.session_state.keys():
                if key == 'login_disabled' or key == 'logout_disabled':
                    st.session_state[key] = not st.session_state[key]
                else:
                    st.session_state[key] = ''
            st.session_state.login_disabled = False
            st.session_state.username = ''
            query_params = st.experimental_get_query_params()
            query_params["access_token"] = None
            st.experimental_set_query_params(**query_params)

def main():
    if login():
        st.markdown("<h1 style='text-align: center;'>Geospatial Data Exploration Tool 🔭</h1>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()