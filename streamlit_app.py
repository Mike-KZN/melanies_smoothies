# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie App :cup_with_straw:")

st.write("Choose the fruits you want in your custom Smoothie:")

# Input for the name on the smoothie order
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe['FRUIT_NAME'].tolist(),
    max_selections = 5
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
        
# New section to display FruityVice Nutrician Information
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# st.text(fruityvice_response.json())
fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=TRUE)
