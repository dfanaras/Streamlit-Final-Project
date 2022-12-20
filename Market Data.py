import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pydeck as pdk

st.set_page_config(page_title='Information',
                   page_icon=':bar-chart:',
                   layout='wide')

st.title('Charting Data')
chart = st.radio('Select what data you would like to see:', ['Average Listing Price by Manufacturer', 'Trend of Mileage by Year', 'Percentage of colors in marketplace'])

def create_DataFrame(file=r'C:\Users\mfana\PycharmProjects\pythonProject\Final Project\craigslist_dataset.csv'):
    read_result = pd.read_csv(file)
    dataframe = pd.DataFrame(read_result)
    dataframe.set_index(['id'], inplace=True)
    del dataframe['Unnamed: 0']
    del dataframe['description']
    return dataframe

data = create_DataFrame() #to get referenceable dataframe from function


if chart == 'Percentage of colors in marketplace':
    filter = st.sidebar.multiselect('Choose manufacturer(s) to see percentage of colors available:', ['acura', 'alfa-romeo', 'audi', 'bmw', 'buick', 'cadillac', 'chevrolet', 'chrysler', 'dodge', 'ferrari', 'fiat', 'ford', 'gmc', 'harley-davidson', 'honda', 'hyundai', 'infiniti', 'jaguar', 'jeep', 'kia', 'lexus', 'lincoln', 'mazda', 'mercedes-benz', 'mercury', 'mini', 'mitsubishi', 'nissan', 'pontiac', 'porsche', 'ram', 'rover', 'saturn', 'subaru', 'tesla', 'toyota', 'volkswagen', 'volvo'], key='filter')

    dataq = data.query("manufacturer == @filter")
    p1 = dataq["paint_color"].value_counts()

    fig = plt.figure(figsize=(12, 8))
    a1 = fig.add_axes([.1,.6, .3, .3])

    a1.pie(p1, labels=p1.keys(), autopct="%.1f%%")
    plt.title('Percentage Cars in a Specific Color')
    st.pyplot(fig)


if chart == 'Average Listing Price by Manufacturer':
    filter = st.sidebar.number_input('You can filter the chart buy average listing price', 0, 150000)
    df = data.loc[:,['manufacturer','price']]
    df1 = df.groupby(by = ['manufacturer']).mean()
    yaxis = []
    for index in df1.index:
        if df1['price'][index] > filter:
            yaxis.append(df1['price'][index])
        xaxis = []
    for index in df1.index:
        if df1['price'][index] in yaxis:
            xaxis.append(index)

    import random
    color = 'bgrcmyk'

    fig = plt.bar(xaxis,yaxis,width=.5, color = [random.choice(color) for make in xaxis]) #random.choice makes it so that everytime the graph repopulates based on the filter value, the colors of the bars will be random
    plt.xlabel('Vehicle Manufactuer')
    plt.ylabel('Average Listing Price')
    plt.title('Average Listing Price by Manufacturer')
    plt.xticks(fontsize=2.4) #to make data labels smaller
    st.set_option('deprecation.showPyplotGlobalUse', False) # to remove error message on streamlit
    st.pyplot()


if chart == 'Trend of Mileage by Year':
    df = data.loc[:,['year','odometer']]
    df1 = df.groupby(by = ["year"]).mean()
    yaxis = []
    for index in df1.index:
        if df1['odometer'][index] > 0:
            yaxis.append(df1['odometer'][index])
    xaxis = []
    for index in df1.index:
        if df1['odometer'][index] in yaxis:
            xaxis.append(index)

    import random
    color = 'rbc'

    fig = plt.plot(xaxis,yaxis, linestyle= '-', marker="D" ,color = random.choice(color)) #random.choice makes it so that everytime the graph repopulates based on the filter value, the colors of the bars will be random
    plt.xlabel('Vehicle Manufactuer')
    plt.ylabel('Average Listing Price')
    plt.title('Average Listing Price by Manufacturer')

    st.pyplot()








