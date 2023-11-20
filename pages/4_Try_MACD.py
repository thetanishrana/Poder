import streamlit as st
from streamlit.components.v1 import html
from datetime import date
import time

import numpy as np
import pandas as pd

import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import matplotlib.pyplot as plt

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('MACD Stock Analysis')

# Allow users to input any stock symbol
stock_symbol = st.text_input('Enter stock symbol (e.g., AAPL):')

if not stock_symbol:
    st.warning('Please enter a stock symbol.')
    st.stop()

# Load data with a progress bar
progress_bar = st.progress(0)  # Initialize the progress bar


def load_data_with_progress(ticker):
    @st.cache_data
    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        return data

    data_load_state = st.text('Loading data...')
    data = load_data(ticker)
    data_load_state.text('')

    # Simulate loading progress
    for i in range(100):
        time.sleep(0.01)  # Simulate some processing time
        progress_bar.progress(i + 1)  # Update the progress bar

    return data


# Call the function outside of any st element
data = load_data_with_progress(stock_symbol)

# Calculate MACD and Signal Line
data['26ema'] = data['Close'].ewm(span=26, adjust=False).mean()
data['12ema'] = data['Close'].ewm(span=12, adjust=False).mean()
data['MACD'] = data['12ema'] - data['26ema']
data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()

# tabs
tab1, tab2 = st.tabs(["Historic Closing Price", "Current Raw Data"])

with tab1:
    # Display closing prices as a single line chart
    fig_closing_prices = go.Figure()
    fig_closing_prices.add_trace(go.Scatter(
        x=data['Date'], y=data['Close'], mode='lines', name='Closing Prices'))
    fig_closing_prices.layout.update(
        title_text='Closing Prices Over Time', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig_closing_prices)

with tab2:
    # Display raw data
    st.subheader('Raw Data')
    st.write(data.tail())


# Function to calculate MACD strategy
def MACD_Strategy(df, risk):
    MACD_Buy = []
    MACD_Sell = []
    position = False

    for i in range(0, len(df)):
        if df['MACD'][i] > df['Signal_Line'][i]:
            MACD_Sell.append(np.nan)
            if not position:
                MACD_Buy.append(df['Close'][i])
                position = True
            else:
                MACD_Buy.append(np.nan)
        elif df['MACD'][i] < df['Signal_Line'][i]:
            MACD_Buy.append(np.nan)
            if position:
                MACD_Sell.append(df['Close'][i])
                position = False
            else:
                MACD_Sell.append(np.nan)
        elif position and df['Close'][i] < MACD_Buy[-1] * (1 - risk):
            MACD_Sell.append(df["Close"][i])
            MACD_Buy.append(np.nan)
            position = False
        elif position and df['Close'][i] < df['Close'][i - 1] * (1 - risk):
            MACD_Sell.append(df["Close"][i])
            MACD_Buy.append(np.nan)
            position = False
        else:
            MACD_Buy.append(np.nan)
            MACD_Sell.append(np.nan)

    df['MACD_Buy_Signal_price'] = MACD_Buy
    df['MACD_Sell_Signal_price'] = MACD_Sell


# Call the MACD_Strategy function
MACD_Strategy(data, 0.025)

# Plot MACD and Signal Line along with Buy and Sell signals
st.subheader('MACD and Signal Line with Buy/Sell Signals')
fig_macd_strategy = go.Figure()
fig_macd_strategy.add_trace(go.Scatter(
    x=data['Date'], y=data['MACD'], mode='lines', name='MACD', line=dict(color='white', width=2)))
fig_macd_strategy.add_trace(go.Scatter(
    x=data['Date'], y=data['Signal_Line'], mode='lines', name='Signal Line', line=dict(color='darkgray', width=2)))
buy_signals = data[data['MACD_Buy_Signal_price'].notna()]
sell_signals = data[data['MACD_Sell_Signal_price'].notna()]
fig_macd_strategy.add_trace(go.Scatter(x=buy_signals['Date'], y=buy_signals['MACD'],
                                       mode='markers', marker=dict(symbol='triangle-up', size=10, color='green'),
                                       name='Buy Signal'))
fig_macd_strategy.add_trace(go.Scatter(x=sell_signals['Date'], y=sell_signals['MACD'],
                                       mode='markers', marker=dict(symbol='triangle-down', size=10, color='red'),
                                       name='Sell Signal'))
fig_macd_strategy.update_layout(
    title_text='MACD and Signal Line with Buy/Sell Signals', xaxis_rangeslider_visible=True)
st.plotly_chart(fig_macd_strategy)

def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)

if st.button("< Go Back"):
    nav_page("Strategy")