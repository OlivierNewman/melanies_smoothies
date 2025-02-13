# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
# Write directly to the app
st.title("Customize your smoothie :cup_with_straw:")
st.write(
    """Please choose what you would like in your smoothie
    """
)


name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be", name_on_order)


# option = st.selectbox(
#     "What is your favorite fruit",
#     ("Bannanas", "Strawberries", "Peaches"),
# )


# st.write("You selected:", option)
cnx =st.connection("snowflake")
session = cnx.session()
#st.write(session)
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")#.select(col('Fruit_Name'))
st.dataframe(data=my_dataframe, use_container_width=True)




ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections= 6
)
if ingredients_list:                                 
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen +' '
        
    st.write(ingredients_string)
    st.write('For' + ' ' + name_on_order)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!' + ' '+ name_on_order, icon="✅")


 #insert into smoothies.public.orders(ingredients,name_on_order) values ('Dragon Fruit Guava Jackfruit Kiwi ','MellyMel')
 



