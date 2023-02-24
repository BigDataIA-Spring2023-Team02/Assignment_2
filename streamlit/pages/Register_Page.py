import streamlit as st
import requests
import json
from streamlit_extras.switch_page_button import switch_page

if 'first_name' not in st.session_state:
    st.session_state.first_name = ''

if 'last_name' not in st.session_state:
    st.session_state.last_name = ''

if 'username' not in st.session_state:
    st.session_state.username = ''

if 'password' not in st.session_state:
    st.session_state.password = ''

if 'access_token' not in st.session_state:
    st.session_state.access_token = ''

if 'register_disabled' not in st.session_state:
    st.session_state.register_disabled = False

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    
if 'logout_disabled' not in st.session_state:
    st.session_state.logged_in = True

first_name = st.text_input("First Name", st.session_state.first_name, placeholder='First Name')
last_name = st.text_input("Last Name", st.session_state.last_name, placeholder='Last Name')
username = st.text_input("Username", st.session_state.username, placeholder='Username')
password = st.text_input("Password", st.session_state.password, placeholder='Password', type = 'password')
register_submit = st.button('Register', disabled = st.session_state.register_disabled)

if register_submit:
    st.session_state.first_name = first_name
    st.session_state.last_name = last_name
    st.session_state.username = username
    st.session_state.password = password
    register_user = {
        'first_name': st.session_state.first_name,
        'last_name': st.session_state.last_name,
        'username': st.session_state.username,
        'password': st.session_state.password
    }
    res = requests.post(url='http://localhost:8000/users', data=json.dumps(register_user))
    if res and res.status_code == 200:
        st.session_state.access_token = res.json()['access_token']
        st.session_state.register_disabled = True
        st.session_state.logged_in = True
        st.session_state.logout_disabled = False
        switch_page('GEOS18_Page')
    else:
        st.error("Error: User registration failed!")

with st.sidebar:
    if st.session_state and st.session_state.logged_in and st.session_state.username:
        st.write(f'Current User: {st.session_state.username}')
    else:
        st.write('Current User: Not Logged In')