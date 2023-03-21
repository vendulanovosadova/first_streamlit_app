import streamlit
import pandas
import requests
import snowflake.connector 
from urllib.error import URLError 
streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🐔 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞🐔 Avocado Toast')
streamlit.header('🍌🥑 Build Your Own Fruit Smoothie 🥝🍇')

# let's add CSV file with fruit info ---- CSV table part
#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include, they choose a fruit by a number, or you can manually code the fruit you like to select 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]                        #<<<< as per your selection, it will return info from CSV file with nutrition info

# Display the table on the page.
streamlit.dataframe(fruits_to_show) #<<< this shows the CSV breakdown below the table

#-----------------------------------------------------------------------------------------------------------------------------------------------

#New section to display fruityvice api response - FIRST ROW WITH MANUAL INPUT
streamlit.header('Fruityvice Fruit Advice!')
try:
     fruit_choice = streamlit.text_input('What fruit would you like information about?')         #<<< ROW WITH MANUAL INPUT, we call in fruit_choice row
     if not fruit_choice:
        streamlit.error ("Please select a fruit to get information.")
     else:                                                                                       #<< these are STEPS which will be REPEATING!!!
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())                 #<< take the json version of the response and normalize it  
        streamlit.dataframe(fruityvice_normalized)                                                #<< output it the screen as the table  
 
except URLError as e:
    streamlit.error()
      

     
             

#don't run anything past this while we troubleshoot
streamlit.stop()
import snowflake.connector                                                 # imports Snowflake table "fruit_load_list"
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])     #<<< references setting in Streamlit app, where we put password to connect with Snowflake
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")           #<<< this is a Snowflake table, into which people also add manually via Streamlit app
my_data_rows = my_cur.fetchall()                          #<<< selects all rows from the table from Snowflake, still adds a manual input from the Streamlit app. 
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

#New section to display fruityvice api response
add_my_fruit = streamlit.text_input('What fruit would you like information about?','jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit) #<<<< here we set up the end user enters the fruit manually

#This will not work correctly, but just go with it for now
#my_cur_execute("insert into fruit_load_list values ('from Streamlit')") #<< this is a trouble allowing me to input data from Streamlit app directly






