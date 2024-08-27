# Import Python packages
import streamlit as st
import pandas as pd
import snowflake.connector
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie App :cup_with_straw:")

st.write("Choose the fruits you want in your custom Smoothie:")

# Input for the name on the smoothie order
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", name_on_order)

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

# Convert the Snowpark DataFrame to a Pandas DataFrame so we can use the LOC function
pd_df = my_dataframe.to_pandas()

st.dataframe(pd_df)  # Optional: display the DataFrame for debugging
st.stop()  # Optional: stop execution for debugging

# Use a multiselect widget in Streamlit to allow users to select up to 5 ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'],
    max_selections=5
)

# Check if any ingredients were selected
if ingredients_list:
    ingredients_string = ''

    # Loop through the selected ingredients
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)

        # Display the data fetched from the API in a Streamlit dataframe
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
