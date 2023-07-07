#create main python file
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('New movie play list')

streamlit.header(':calendar: Hollywood :movie_camera:')
streamlit.text('🎞️ Secret life of milley walter')
streamlit.text('🎬 Silent Voice')
streamlit.text('📹 The space between us')
streamlit.text('📽️ Upside down')

# Display the table on the page.
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.header('Healthy fruits')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(t):
  r=requests.get("https://fruityvice.com/api/fruit/"+t)
  n=pandas.json_normalize(r.json())
  return n

streamlit.header("View Our Fruit List - Add Your Favorites!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    fuct_res = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fuct_res)
    #streamlit.write('The user entered ', fruit_choice)
except URLError as e:
  streamlit.error()

def get_fruit_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

if streamlit.button('Get fruit List'):
  my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows=get_fruit_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

#streamlit.stop()
def insert_row(nf):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values('"+nf+"')")
    return "Thanks for adding "+nf
  
add_my_fruit = streamlit.text_input('what fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
  my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
  fuc_insert_res=insert_row(add_my_fruit)
  streamlit.text(fuc_insert_res)
