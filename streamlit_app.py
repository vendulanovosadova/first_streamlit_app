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

#create a repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())                 #<< take the json version of the response and normalize it  
        return fruityvice_normalized

#New section to display fruityvice api response                                                   #<< FIRST ROW WITH MANUAL INPUT
streamlit.header('Fruityvice Fruit Advice!')
try:
     fruit_choice = streamlit.text_input('What fruit would you like information about?')          #<< ROW WITH MANUAL INPUT, we call in fruit_choice row
     if not fruit_choice:
        streamlit.error ("Please select a fruit to get information.")
     else:                                                                                        #<< these are STEPS which will be REPEATING!!!
         back_from_function = get_fruityvice_data(fruit_choice)
         streamlit.dataframe(back_from_function)                                                  #<< output it the screen as the table  
 
except URLError as e:
    streamlit.error()
      
streamlit.header("The fruit load list contains:")
#Snowflake-related functions
def get_fruit_load_list():                                                     #<<< function that queries the table
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select * from fruit_load_list")
         return my_cur.fetchall() 

#Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):                                    #<< button that calls our function and loads the data onto the page. 
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])   #<<<setting in Streamlit app, where we put password to connect with Snowflake        
      my_data_rows = get_fruit_load_list()                       
      streamlit.dataframe(my_data_rows)   
        
#Allow the end user to add fruit to the list manually -------
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load_list values ('from streamlit')")
         return "Thanks for adding "+new_fruit
                              
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])     
   back_from_function = insert_row_snowflake(add_my_fruit)
   streamlit.text(back_from_function)       
           
        
        
        
        

#don't run anything past this while we troubleshoot-------------------------------
streamlit.stop()
import snowflake.connector                                                 # imports Snowflake table "fruit_load_list"

my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")           #<<< this is a Snowflake table, into which people also add manually via Streamlit app

streamlit.write('Thanks for adding ', add_my_fruit)                        

#This will not work correctly, but just go with it for now
#my_cur_execute("insert into fruit_load_list values ('from Streamlit')")           #<< this is a trouble allowing me to input data from Streamlit app directly






