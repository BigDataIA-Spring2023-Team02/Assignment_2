import os
import boto3
import requests
import streamlit as st
from dotenv import load_dotenv
from requests.exceptions import HTTPError
from fastapi.security import OAuth2PasswordBearer
from streamlit_extras.switch_page_button import switch_page

#load env variables
load_dotenv()

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