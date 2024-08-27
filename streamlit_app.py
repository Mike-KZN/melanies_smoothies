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

# Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

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

        # Use .loc to find the corresponding 'SEARCH_ON' value for the selected fruit
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        
        # Display the search value using Streamlit's write function
        st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')

        # Display a subheader for each selected fruit
        st.subheader(fruit_chosen + ' Nutrition Information')

        # Make a request to the Fruityvice API to fetch nutrition information for the selected fruit
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)

        # Display the data fetched from the API in a Streamlit dataframe
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

