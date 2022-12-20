''' Final Project by: David Fanaras '''

import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pydeck as pdk
st.set_page_config(page_title='Craigslist Car Finder',
                   page_icon=':car:',
                   layout='wide')

st.title('Welcome to the Car Finder!')

def create_DataFrame(file=r'C:\Users\mfana\PycharmProjects\pythonProject\Final Project\craigslist_dataset.csv'): #Function with default parameter that returns a value
    read_result = pd.read_csv(file)
    dataframe = pd.DataFrame(read_result)
    dataframe.set_index(['id'], inplace=True)
    del dataframe['Unnamed: 0']
    del dataframe['description']
    return dataframe

data = create_DataFrame() #to get referenceable dataframe from function


pricelist = []
for price in data['price']: #to get all listings that have a real price
    if price > 0: #to get all values except listings without a price
        pricelist.append(price)


st.sidebar.markdown("# Price Filter")
price = st.sidebar.slider('Select your budget: ', 0, max(pricelist), key='price',)
st.sidebar.write(f"The filtered results will show cars up to ${price} in value")


st.sidebar.markdown('# Mileage Filter')
miles = st.sidebar.number_input('Choose the maximum amount of miles that would be on your car', step=100, key='mileage')
st.sidebar.write(f"The filtered results will show cars with {miles} miles or less ")


colorlist = []
for color in data['paint_color']: #loop to get all of the different colors of the cars for sale, will add to the list if new color is added into the dataset
    if color not in colorlist and type(color) == str:
        colorlist.append(color)
        colorlist = sorted(colorlist)

st.sidebar.markdown('# Color(s) Filter')
color = st.sidebar.multiselect(f"What color(s) would you like? ",colorlist ,key='colors')
st.sidebar.write(f"The filtered results will show cars in {color}")


makelist = [] # to get list of unique values to add to the multiselect. If a new listing is added where the make is not already in the list, it will be automatically added
x=[makelist.append(make) for make in data['manufacturer'] if make not in makelist and type(make) == str] #list comprehension
makelist = sorted(makelist)


st.sidebar.markdown('# Make Filter')
make = st.sidebar.multiselect('Choose manufacturer(s): ', makelist, key='make')
st.sidebar.write(f"The filtered results will show cars manufactured by {make}")

def filtered_dataframe(): #meat of the project, takes all values in specifc column and compares them to the session state value and adjusts the data frame according to filters
        newdf = data[(data['price'] <= st.session_state.price) &
                 (data['manufacturer'].isin(st.session_state.make)) &
                 (data['odometer'] <= st.session_state.mileage) &
                 (data['paint_color'].isin(st.session_state.colors))] #isin function is basically a for loop that iterates through the list of values of the colors key in the session state list

        return newdf

chartdf = filtered_dataframe()


st.dataframe(filtered_dataframe()) #filtered dataframe
st.write(f"There are {len(chartdf)} listings that meet your search criteria")

chartdf.rename(columns={"lat": "lat", "long": "lon"}, inplace=True) #this is because st.map only recognizes "lat" and "lon"


longlat = chartdf.loc[:,["lat",'lon']]
longlat = longlat.dropna()
st.title('This is where your dream car is!')
st.map(longlat)




### PYDECK MAP ###

data = longlat
ICON_URL = r'C:\Users\mfana\PycharmProjects\pythonProject\Final Project\640px-Emoji_u1f698.png'
chartdf.rename(columns={"lat": "lat", "long": "lon"}, inplace=True)

data = chartdf.dropna()

#formatting icon
icondata = {'file':ICON_URL,
            'width': 100,
            'height': 100,
            'anchorY': 100
            }

data = data.loc[:,['lat','lon',]]
data = data.dropna()
#create view of the map
viewstate = pdk.ViewState(latitude=data['lat'].mean(),
                          longitude=data['lon'].mean(),
                          zoom=11,
                          pitch=10)

data['icondata'] = None

for i in data.index:
    data['icondata'][i] = icondata

data = data.loc[:,['lat','lon','icondata']]
data = data.dropna()


#create layer with custom icon
iconlayer = pdk.Layer(type='IconLayer',
                      data= data,
                      get_icon= icondata,
                      get_position='[lat, lon]',
                      get_size=4,
                      size_scale=10)


map = pdk.Deck(map_style= 'mapbox://styles/mapbox/outdoors-v12',
               initial_view_state = viewstate,
               layers = [iconlayer])


st.pydeck_chart(map)


