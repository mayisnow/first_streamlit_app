import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show=my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information!")
  else:
    back_from_function=get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()
#streamlit.stop()

def get_fruit_load_list():
      with my_cnx.cursor() as my_cur:
           my_cur.execute("SELECT * from FRUIT_LOAD_LIST")
           return my_cur.fetchall()
      
if streamlit.button('Get Fruit Load List'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets['snowflake'])
      my_data_row = get_fruit_load_list()
      streamlit.dataframe(my_data_row)
def insert_new_snowflake(new_fruit):
      with my_cnx.cursor() as my_cur:
           my_cur.execute("insert into FRUIT_LOAD_LIST values ('" + new_fruit +"')")
           return 'Thanks for adding '+ new_fruit
add_fruit = streamlit.text_input('Which fruit would you like to add?')
if streamlit.button('Add a fruit to List'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets['snowflake'])
      back_from_function=insert_new_snowflake(add_fruit)
      streamlit.text(back_from_function)
