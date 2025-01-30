# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
 
# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your Customize Smoothie!
    """
)
 
 
Name_on_order = st.text_input("Name on Smopthie:")
st.write("Name on your Smoothie will be:", Name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()
 
 
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
# st.dataframe(data=my_dataframe, use_container_width=True)
 
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients :"
    , my_dataframe
    , max_selections = 5)
 
if ingredients_list:
     ingredients_string = ''
     for fruit_chosen in ingredients_list:
         ingredients_string += fruit_chosen + ' '
 
     # st.write(ingredients_string)
 
     my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+ Name_on_order +"""')"""
 
     #st.write(my_insert_stmt)
     # st.stop()
     time_to_insert = st.button('Submit order')
 
     if time_to_insert:
         session.sql(my_insert_stmt).collect()
         st.success(f'Your Smoothie is ordered , {Name_on_order}!', icon="✅")

#New section to display soomthiefruit nutrition information
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())
