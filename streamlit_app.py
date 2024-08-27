import streamlit as st
import pandas as pd
import requests
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
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie App :cup_with_straw:")

st.write("Choose the fruits you want in your custom Smoothie:")

# Input for the name on the smoothie order
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", name_on_order)
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
        # Find the corresponding 'SEARCH_ON' value
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]

        # Check if the search_on value is different from fruit_chosen to avoid redundancy
        if search_on and search_on.lower() != fruit_chosen.lower():
            sentence = f"The search value for {fruit_chosen} is {search_on}."
        else:
            sentence = f"The search value for {fruit_chosen} is '{search_on or 'Not found'}'."

        # Display the sentence
        st.write(sentence)

        # Display the subheader and fetch the API data
        st.subheader(f"{fruit_chosen} Nutrition Information")

        try:
            fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on or fruit_chosen}")
            fruityvice_response.raise_for_status()

            # Display the data fetched from the API
            st.dataframe(fruityvice_response.json(), use_container_width=True)
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data for {fruit_chosen}: {e}")
