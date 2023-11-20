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

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('SMA Stock Analysis')

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

# Allow users to input parameters for SMA strategy
short_window = st.number_input('Short-term SMA window:', 5, 50, 20, step=1)
long_window = st.number_input('Long-term SMA window:', 50, 200, 50, step=1)

# Option to include a third SMA
include_third_sma = st.checkbox('Include a Third SMA')
if include_third_sma:
    third_long_window = st.number_input(
        'Third Long-term SMA window:', 50, 200, 100, step=1)

# Generate SMA signals
data['Short_SMA'] = data['Close'].rolling(
    window=short_window, min_periods=1, center=False).mean()
data['Long_SMA'] = data['Close'].rolling(
    window=long_window, min_periods=1, center=False).mean()

# Include the third SMA if checkbox is selected
if include_third_sma:
    data['Third_Long_SMA'] = data['Close'].rolling(
        window=third_long_window, min_periods=1, center=False).mean()

# Generate signals
data['Signal'] = 0.0

if include_third_sma:
    # Use all three SMAs when the third SMA is included
    data['Signal'][short_window:] = np.where(
        (data['Short_SMA'][short_window:] > data['Long_SMA'][short_window:]) &
        (data['Short_SMA'][short_window:] > data['Third_Long_SMA'][short_window:]), 1.0, 0.0)
else:
    # Use only the first two SMAs when the third SMA is not included
    data['Signal'][short_window:] = np.where(
        data['Short_SMA'][short_window:] > data['Long_SMA'][short_window:], 1.0, 0.0)

# Generate trading orders
data['Position'] = data['Signal'].diff()

# Analyze historic data and mark buy/sell signals with icons
buy_signals = data[data['Position'] == 1]
sell_signals = data[data['Position'] == -1]

# Plot buy and sell signals with up and down triangles
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=data['Date'], y=data['Close'], name="Stock Close", line=dict(color='white')))
fig.add_trace(go.Scatter(x=buy_signals['Date'], y=buy_signals['Close'],
              mode='markers', name='Buy Signal', marker=dict(symbol='triangle-up', color='green', size=8,
                                                             line=dict(color='green', width=1))))
fig.add_trace(go.Scatter(x=sell_signals['Date'], y=sell_signals['Close'],
              mode='markers', name='Sell Signal', marker=dict(symbol='triangle-down', color='red', size=8,
                                                              line=dict(color='red', width=1))))
fig.layout.update(title_text='Buy and Sell Signals',
                  xaxis_rangeslider_visible=True)
st.plotly_chart(fig)

# Plot SMA comparison graph
st.subheader('SMA Comparison')
fig_sma = go.Figure()
fig_sma.add_trace(go.Scatter(
    x=data['Date'], y=data['Short_SMA'], name=f'Short-term SMA ({short_window})'))
fig_sma.add_trace(go.Scatter(
    x=data['Date'], y=data['Long_SMA'], name=f'Long-term SMA ({long_window})'))

# Include the third SMA if checkbox is selected
if include_third_sma:
    fig_sma.add_trace(go.Scatter(
        x=data['Date'], y=data['Third_Long_SMA'], name=f'Third Long-term SMA ({third_long_window})'))

fig_sma.layout.update(title_text='SMA Comparison',
                      xaxis_rangeslider_visible=True)
st.plotly_chart(fig_sma)

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
