import streamlit as st
import pandas as pd
import json
import requests
from streamlit_lottie import st_lottie 

url = requests.get( 
    "https://lottie.host/5c7fe2a7-9a88-4ba8-8d47-9df289077e49/T4Ec66vEGw.json")

url_json = dict() 

if url.status_code == 200: 
    url_json = url.json() 
else: 
    print("Error in the URL") 

st.title("Technical Analysis Learning Roadmap")

st.header("Top 20 Stock Exchanges in the World")

    # Sample data for the top 20 stock exchanges
data = {
    'Name of Exchange                                       ': ['NYSE', 'NASDAQ', 'Tokyo Stock Exchange', 'London Stock Exchange', 'Shanghai Stock Exchange',
                         'Hong Kong Stock Exchange', 'Euronext', 'Shenzhen Stock Exchange', 'TMX Group', 'Frankfurt Stock Exchange',
                         'Bombay Stock Exchange', 'SIX Swiss Exchange', 'BM&F Bovespa', 'Australian Securities Exchange',
                         'National Stock Exchange of India', 'Korea Exchange', 'Johannesburg Stock Exchange', 'Taiwan Stock Exchange',
                         'Madrid Stock Exchange', 'Moscow Exchange'],
    'Market Cap (in Billion USD)': [31.85, 20.30, 6.262, 4.755, 4.420, 4.018, 3.918, 3.551, 2.614, 1.956, 1.867, 1.763, 1.573, 1.561, 1.501, 1.420, 1.305, 1.198, 1.113, 1.042],
    'Currency': ['USD', 'USD', 'JPY', 'GBP', 'CNY', 'HKD', 'EUR', 'CNY', 'CAD', 'EUR', 'INR', 'CHF', 'BRL', 'AUD', 'INR', 'KRW', 'ZAR', 'TWD', 'EUR', 'RUB'],
    'City': ['New York', 'New York', 'Tokyo', 'London', 'Shanghai', 'Hong Kong', 'Amsterdam', 'Shenzhen', 'Toronto', 'Frankfurt',
             'Mumbai', 'Zurich', 'Sao Paulo', 'Sydney', 'Mumbai', 'Seoul', 'Johannesburg', 'Taipei', 'Madrid', 'Moscow'],
    'Country': ['USA', 'USA', 'Japan', 'UK', 'China', 'Hong Kong', 'Netherlands', 'China', 'Canada', 'Germany', 'India', 'Switzerland',
                'Brazil', 'Australia', 'India', 'South Korea', 'South Africa', 'Taiwan', 'Spain', 'Russia'],
    'LAT': [40.7128, 40.7128, 35.6895, 51.5099, 31.2304, 22.3964, 52.3676, 22.5431, 43.6532, 50.1109, 19.0760, 47.3769, -23.5505, -33.8688,
                 19.0760, 37.5665, -26.2041, 25.0320, 40.4168, 55.7558],
    'LON': [-74.0060, -74.0060, 139.6917, -0.1180, 121.4737, 114.1095, 4.9041, 114.0579, -79.3832, 8.6821, 72.8777, 8.5417, -46.6333, 151.2093,
                  72.8777, 126.9780, 28.0473, 121.5654, -3.7038, 37.6176]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Display a map
st.map(df[['LAT', 'LON']])

# Set the index to start from 1
df.index = range(1, len(df) + 1)



# Display the DataFrame without LAT and LON
st.dataframe(df.drop(columns=['LAT', 'LON']))

# Introduction
st.header("Introduction")
st.write("Welcome to the Technical Analysis Learning Roadmap! This roadmap will guide you through the key concepts and techniques in technical analysis.")

# Beginner Level
with st.container():
    with st.expander("Beginner Level"):
        st.subheader("1. Understanding Stock Charts")
        st.write("Watch this video to understand the basics of stock charts:")
        st.link_button("Stock Charts Basics", "https://www.forbes.com/advisor/investing/how-to-read-stock-charts/#:~:text=A%20stock%20chart%20is%20a,hours%20to%20months%20and%20years.")
        st.subheader("2. Introduction to Candlestick Patterns")
        st.write("Learn about candlestick patterns with this video:")
        st.link_button("Candlestick Patterns", "https://school.stockcharts.com/doku.php?id=chart_analysis:introduction_to_candlesticks")

# Intermediate Level
with st.container():
    with st.expander("Intermediate Level"):
        st.subheader("3. Trend Analysis and Support/Resistance")
        st.write("Explore trend analysis and support/resistance levels:")
        st.link_button("Trend Analysis", "https://www.investopedia.com/trading/support-and-resistance-basics/")
        st.subheader("4. Moving Averages")
        st.write("Understand moving averages and their significance:")
        st.link_button("Moving Averages", "https://www.investopedia.com/terms/m/movingaverage.asp#:~:text=A%20moving%20average%20is%20a,price%20trends%20for%20specific%20securities.")

# Advanced Level
with st.container():
    with st.expander("Advance Level"):
        st.subheader("5. Technical Indicators (RSI, MACD)")
        st.write("Dive into popular technical indicators like RSI and MACD:")
        st.link_button("Technical Indicators", "https://www.valutrades.com/en/blog/how-to-use-macd-and-rsi-together-to-spot-buying-opportunities")
        st.subheader("6. Chart Patterns")
        st.write("Learn about advanced chart patterns and their implications:")
        st.link_button("Chart Patterns", "https://www.investopedia.com/articles/technical/112601.asp")

# Conclusion
st.subheader("Congratulations! You have completed the Technical Analysis Learning Roadmap.")
st_lottie(url_json)