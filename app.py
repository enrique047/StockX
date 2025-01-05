from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.express as px
import datetime as dt
from keras.models import load_model
from pandas_datareader import data as pdr
import streamlit as st
import streamlit.components.v1 as com
import random as ran
from newsapi import NewsApiClient
import pycountry

         

st.set_page_config(
    page_title="StockX"
)  


st.sidebar.title('Navigation')


def prediction():
    
    end = dt.date.today()
    start = end - dt.timedelta(days=3650)

    st.title('Stock Trend Prediction')

    stocks = pd.read_csv('Output 2.csv')
    stocks_list = stocks['Ticker'].values.tolist()

    yf.pdr_override()
    user_input = st.selectbox("Enter Stock Ticker", stocks_list, 0)
    df = pdr.DataReader(user_input, start, end)
    df = df.reset_index()
################################################################## Describing Data ############################################################
    st.subheader(str(user_input) + ' from ' + str(start) + ' to ' + str(end))
    st.write(df.describe())

################################################################### Data Insertion #########################################################
    ma100 = df.Close.rolling(100).mean()
    ma200 = df.Close.rolling(200).mean()
    df.insert(3, "Moving average 100", ma100)
    df.insert(4, "Moving average 200", ma200)
################################################################### Visulalizations #########################################################


    st.subheader('Closing Price Vs Time Chart with 100 Moving Average')
    fig = px.line(df, x=df.Date, y=['Close', 'Moving average 100'])
    st.write(fig)

    st.subheader('Closing Price Vs Time Chart with 200 Moving Average')
    fig2 = px.line(df, x=df.Date,y=['Close', 'Moving average 100', 'Moving average 200'])
    st.write(fig2)


######################################################### Data Spliting and Scaling ########################################################

    data_training = pd.DataFrame(df['Close'][0:int(0.5*len(df))])
    data_testing = pd.DataFrame(df['Close'][int(0.5*len(df)):int(len(df))])

    scaler = MinMaxScaler(feature_range=(0, 1))  # Scaling

    data_training_array = scaler.fit_transform(data_training)  # fitting

    model = load_model('new_model.h5')  # Loding the Model


############################################################### Testing #####################################################################
    past_100_days = data_training.tail(100)
    final_df = past_100_days.append(data_testing, ignore_index=True)
    input_data = scaler.fit_transform(final_df)

    x_test = []
    y_test = []

    for i in range(100, input_data.shape[0]):
        x_test.append(input_data[i-100: i])
        y_test.append(input_data[i, 0])

    x_test, y_test = np.array(x_test), np.array(y_test)

############################################################## prdeiction ###############################################################
    y_predicted = model.predict(x_test)
    scaler = scaler.scale_
    scale_factor = 1.29/scaler[0]
    y_predicted = y_predicted * scale_factor
    y_test = y_test * scale_factor

    y_predicted = y_predicted.reshape(-1)
############################################################ Final Graph For Prediction ##########################################################
    temp_data = list(zip(df.Date[y_test.shape[0]: df.shape[0]], y_test, y_predicted))
    pre = pd.DataFrame(temp_data, columns=['Date', 'Testing Data', 'Prediction'])

    st.subheader('Prediction V/s Original Price')
    fig3 = px.line(pre, x=pre.Date, y=['Testing Data', 'Prediction'])
    st.write(fig3)
###################################################################################################################################################
    dataPrintList=pre.iloc[-1].tolist()
    st.subheader('The Estimated Closing price for '+str(dataPrintList[0])+' :')
    st.subheader(str(dataPrintList[2]))
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("Disclaimer:")
    st.write("The provided value can have a margin of error upto 20%. The information provided in this content is for informational purposes only and should not be construed as financial advice. Readers are advised to consult with a licensed financial advisor before making any investment decisions. The opinions expressed in this content are solely those of the author and do not reflect the opinions of any financial institutions or organizations. Any investment decisions made based on the information provided are made at the reader's own risk, and neither the author nor their company will be held responsible for any losses or damages that may result.")





def home():
    st.title('StockX')
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("When it comes to investing, nothing will pay off more than educating yourself.")
    st.write("Do the necessary research and analysis before making any investment decisions.")

def recom():
    st.title('Financial News:') 
    col1,col2=st.columns([10,1])
    newsapi = NewsApiClient(api_key='6674fb22748c4db6acec73629b09ceed') 
    input_country = 'India'
    input_countries = [f'{input_country.strip()}']
    countries = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_2

    codes = [countries.get(country.title(), 'Unknown code')for country in input_countries]


    option='Business'
    top_headlines = newsapi.get_top_headlines(category=f'{option.lower()}', language='en', country=f'{codes[0].lower()}')
    Headlines = top_headlines['articles']

    if Headlines:
        for articles in Headlines:
            b = articles['title'][::-1].index("-")
            if "news" in (articles['title'][-b+1:]).lower():
                news= f"{articles['title'][-b+1:]}: {articles['title'][:-b-2]}."
                col1.markdown(news)
                    
            else:
                news=f"{articles['title'][-b+1:]} News: {articles['title'][:-b-2]}."
                col1.markdown(news)
                    
    else:
        col1.markdown("Sorry no articles found for India, Something Wrong!!!")
     
    



options = st.sidebar.radio('Pages',options=['Home','Prediction','Financial News'])
st.sidebar.success('Click the above options')

if options=='Home':
    home()
elif options=='Prediction':
    prediction()
elif options=='Financial News':
    recom()
