# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie App :cup_with_straw:")

st.write("Choose the fruits you want in your custom Smoothie:")

# Input for the name on the smoothie order
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", name_on_order)

# Establish a connection to Snowflake and retrieve data
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# Convert the Snowpark DataFrame to a Pandas DataFrame
pd_df = my_dataframe.to_pandas()

# Use the Pandas DataFrame for the multiselect widget
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'].tolist(),  # Corrected to use Pandas DataFrame
    max_selections=5
)

if name_on_order and ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    
    my_insert_stmt = f"""
    insert into smoothies.public.orders(name_on_order, ingredients) 
    values ('{name_on_order}', '{ingredients_string}')
    """

    time_to_insert = st.button('Submit Order', key='submit_order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
else:
    if not name_on_order:
        st.warning('Please enter a name for your smoothie.')
    if not ingredients_list:
        st.warning('Please select at least one ingredient.')
        
# New section to display Fruityvice nutrition information
if ingredients_list:
    for fruit_chosen in ingredients_list:
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write(f'The search value for {fruit_chosen} is {search_on}.')
     
        st.subheader(f"{fruit_chosen} Nutrition Information")
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_chosen}")
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
