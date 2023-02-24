import json
import folium
import requests
import warnings
import streamlit as st
import streamlit_folium as stf

warnings.simplefilter(action='ignore', category=FutureWarning)

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
    st.markdown("<h2 style='text-align: center;'>NexRad Map Geo-Locations 📍</h1>", unsafe_allow_html=True)
    
    BASE_URL = "http://localhost:8000"
    
    with st.spinner('Refreshing map locations ...'):
        
        response = requests.request("GET", f"{BASE_URL}/database/mapdata")#, headers=headers)
        if response.status_code == 404:
            st.warning("Unable to fetch mapdata")
            st.stop()
        else:
            json_data = json.loads(response.text)
            map_dict = json_data

        map = folium.Map(location=[40,-100], tiles="OpenStreetMap", zoom_start=4)
        for i in range(0,len(map_dict)):
            folium.Marker(
            location = [map_dict.iloc[i]['latitude'], map_dict.iloc[i]['longitude']],
            popup = (map_dict.iloc[i]['Station_Code'],map_dict.iloc[i]['County'])
            ).add_to(map)

        st.markdown("<h2 style='text-align: center;'>Nexrad Station Pointers</h1>", unsafe_allow_html=True)
        stf.st_folium(map, width=700, height=460)
        
else:
    st.title("Please sign-in to access this feature!")