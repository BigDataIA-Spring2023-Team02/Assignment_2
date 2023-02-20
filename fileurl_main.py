import re
import requests
import streamlit as st

def goes_18_link_generation(file):
    try:
        start_url = "https://noaa-goes18.s3.amazonaws.com/"
        file = file.strip()
        
        if (re.match(r'[O][R][_][A-Z]{3}[-][A-Za-z0-9]{2,3}[-][A-Za-z0-9]{4,6}[-][A-Z0-9]{2,5}[_][G][1][8][_][s][0-9]{14}[_][e][0-9]{14}[_][c][0-9]{14}\b', file)):
            file_name = file.split("_")
            file_split = file_name[1].split('-')
            no_digits = []
            for i in file_split[2]:
                if not i.isdigit():
                    no_digits.append(i)
            str_2 = ''.join(no_digits)
            year = file_name[3][1:5]
            day = file_name[3][5:8]
            hour = file_name[3][8:10]
            selected_file_key = file_name[1][0:7] + str_2 + '/' + year + '/' + day + '/' + hour + '/' + file
            url = start_url + file_split[0] + '-' + file_split[1] + '-' + str_2 + '/' + year + '/' + day + '/' + hour + '/' + file
            response = requests.get(url)
            if(response.status_code == 404):
                raise SystemExit()
            return url, selected_file_key
        else:
            st.error('Please Check Input Filename')
            raise SystemExit()
    
    except:
        st.error('No input Filename')

def nexrad_link_generation(file):
    try:
        start_url = "https://noaa-nexrad-level2.s3.amazonaws.com/"
        file = file.strip()

        if (re.match(r'[A-Z]{3}[A-Z0-9][0-9]{8}[_][0-9]{6}[_]{0,1}[A-Z]{0,1}[0-9]{0,2}[_]{0,1}[A-Z]{0,3}\b', file)):
            selected_file_key = file[4:8] + "/" + file[8:10] + "/" + file[10:12] + "/" + file[:4] + "/" + file
            url = start_url + file[4:8] + "/" + file[8:10] + "/" + file[10:12] + "/" + file[:4] + "/" + file
            response = requests.get(url)
            if(response.status_code == 404):
                raise SystemExit()
            return url, selected_file_key
        else:
            st.error('Please Check Input Filename')
            raise SystemExit()
    
    except:
        st.error('No input Filename')

def goes18_filename_link_generation(product_name, year_input, day_input, hour_input, file_input):
    try:
        selected_file = product_name + '/' + year_input + '/' + day_input + '/' + hour_input + '/' + file_input
        url = "https://noaa-goes18.s3.amazonaws.com/{product_name}/{year_input:04}/{day_input:03}/{hour_input:02}/{file_input}"
        response = requests.get(url)
        if(response.status_code == 404):
            raise SystemExit()
        return url, selected_file
    except:
        st.error('No input Filename')

def nexrad_filename_link_generation(year_input, month_input, day_input, station_code_input, file_input):
    try:
        selected_file = year_input + '/' + month_input + '/' + day_input + '/' + station_code_input + '/' + file_input
        url = "https://noaa-nexrad-level2.s3.amazonaws.com/{year_input:04}/{month_input:02}/{day_input:02}/{station_code_input:02}/{file_input}"
        response = requests.get(url)
        if(response.status_code == 404):
            raise SystemExit()
        return url, selected_file
    except:
        st.error('No input Filename')