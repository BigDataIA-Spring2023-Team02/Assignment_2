import requests
import streamlit as st

# Define the base URL for the FastAPI
base_url = 'http://localhost:8000'

# Define a function to retrieve data from the FastAPI
def get_geos18_data(Product_Name=None, Year=None, Day=None, Hour=None):
    # Build the URL for the API endpoint
    url = f'{base_url}/geos18'

    # Add the query parameters to the URL, if supplied
    if Product_Name:
        url += f'?product={Product_Name}'
        if Year:
            url += f'&year={Year}'
            if Day:
                url += f'&dayofyear={Day}'
                if Hour:
                    url += f'&hour={Hour}'
        elif Day:
            url += f'?dayofyear={Day}'
            if Hour:
                url += f'&hour={Hour}'
        elif Hour:
            url += f'?hour={Hour}'

    # Make the API request and retrieve the data
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error('Error retrieving data from FastAPI.')
        return []

# Define the Streamlit app
def app():
    # Add a title to the app
    st.title('Geos18 Data Explorer')

    # Add input fields for the query parameters
    product_name_input = st.text_input('Product Name')
    year_input = st.number_input('Year', min_value=2000, max_value=2023, step=1)
    day_input = st.number_input('Day', min_value=1, max_value=365, step=1)
    hour_input = st.number_input('Hour', min_value=0, max_value=23, step=1)

    # Add a button to trigger the API request
    if st.button('Retrieve Data'):
        # Retrieve the data from the API
        data = get_geos18_data(Product_Name=product_name_input, Year=year_input, Day=day_input, Hour=hour_input)

        # Display the data in a table
        if len(data) > 0:
            st.write('Data:')
            st.write(data)
        else:
            st.warning('No data found.')