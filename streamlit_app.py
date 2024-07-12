# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your smootie! :cup_with_straw:")

st.write("""Choose the fuites you want in your custom smoothie!""")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on you smoothie will be:', name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data = my_dataframe, use_container_width = True)
# st.stop()
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

ingredients_list = st.multiselect(
    'CHOOSE UP TO 5', my_dataframe
    ,max_selections = 5
)


# # my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
# # my_dataframe = session.table("smoothies.public.orders").collect()
# if my_dataframe:
#     editable_df = st.data_editor(my_dataframe)
#     submitted = st.button('Submit')
#     if submitted:
#         st.success('Someone clicked the button.')
#         og_dataset = session.table("smoothies.public.orders")
#         edited_dataset = session.create_dataframe(editable_df)
#         try:
#             og_dataset.merge(edited_dataset
#                              , (og_dataset['order_uid'] == edited_dataset['order_uid'])
#                              , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
#                             )
#             st.success('Your Smoothie is ordered!', icon="✅")
#         except:
#             st.write('somethings wrong')

# # st.dataframe(data=my_dataframe, use_container_width=True)

if ingredients_list:

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + '  '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition Information')
        try:
            fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
            fruityvice_response.raise_for_status()  # Raises an HTTPError for bad responses
            fv_data = fruityvice_response.json()
            fv_df = st.dataframe(data=fv_data, use_container_width=True)
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data for {fruit_chosen}: {str(e)}")
        except ValueError as e:  # This will catch JSONDecodeError
            st.error(f"Error decoding JSON for {fruit_chosen}: {str(e)}")


