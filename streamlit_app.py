import requests
import streamlit as st
import pandas as pd
import snowflake.connector
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col

# Snowflake connection parameters
conn_params = {
    "account": "UOHBUOI-ZN81948",
    "user": "mikebd",
    "password": "P@ssw0rd6969",
    "warehouse": "COMPUTE_WH",
    "database": "SMOOTHIES",
    "schema": "PUBLIC",
    "role": "SYSADMIN"
}

# Establish a connection to Snowflake
conn = snowflake.connector.connect(**conn_params)
session = Session.builder.configs(conn_params).create()

# Query data from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'],
    max_selections=5
)

if ingredients_list:
    for fruit_chosen in ingredients_list:
        try:
            # Display which fruit is being fetched
            st.write(f"Fetching data for: {fruit_chosen}")

            # Make a request to the Fruityvice API
            fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
            fruityvice_response.raise_for_status()  # This will raise an HTTPError for bad responses

            # Process the API response
            fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data for {fruit_chosen}: {e}")
