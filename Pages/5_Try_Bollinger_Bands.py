import streamlit as st
from streamlit.components.v1 import html
from datetime import date
import time
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
from plotly.subplots import make_subplots

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('Bollinger Bands Stock Analysis')

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

# Bollinger Bands strategy function


def bb_strategy(data):
    bbBuy = []
    bbSell = []
    position = False
    window = 20
    data['BB_Middle'] = data['Close'].rolling(window=window).mean()
    data['BB_Upper'] = data['Close'].rolling(window=window).mean(
    ) + 2 * data['Close'].rolling(window=window).std()
    data['BB_Lower'] = data['Close'].rolling(window=window).mean(
    ) - 2 * data['Close'].rolling(window=window).std()

    for i in range(len(data)):
        if data['Close'][i] < data['BB_Lower'][i]:
            if not position:
                bbBuy.append(data['Close'][i])
                bbSell.append(np.nan)
                position = True
            else:
                bbBuy.append(np.nan)
                bbSell.append(np.nan)
        elif data['Close'][i] > data['BB_Upper'][i]:
            if position:
                bbBuy.append(np.nan)
                bbSell.append(data['Close'][i])
                position = False
            else:
                bbBuy.append(np.nan)
                bbSell.append(np.nan)
        else:
            bbBuy.append(np.nan)
            bbSell.append(np.nan)

    data['bb_Buy_Signal_price'] = bbBuy
    data['bb_Sell_Signal_price'] = bbSell

    return data


# Apply Bollinger Bands strategy
data = bb_strategy(data)

# Create Plotly subplot with Bollinger Bands strategy
fig_bb_strategy = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03,
                                subplot_titles=['Close Price and Bollinger Bands Strategy', 'Bollinger Bands'])

# Plot Close Price and Bollinger Bands strategy
fig_bb_strategy.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close Price', line=dict(color='white')),
                          row=1, col=1)
fig_bb_strategy.add_trace(go.Scatter(x=data['Date'], y=data['bb_Buy_Signal_price'], mode='markers', marker=dict(symbol='triangle-up', size=10, color='green'),
                                     name='Buy Signal'), row=1, col=1)
fig_bb_strategy.add_trace(go.Scatter(x=data['Date'], y=data['bb_Sell_Signal_price'], mode='markers', marker=dict(symbol='triangle-down', size=10, color='red'),
                                     name='Sell Signal'), row=1, col=1)

# Plot Bollinger Bands
fig_bb_strategy.add_trace(go.Scatter(x=data['Date'], y=data['BB_Upper'], mode='lines', name='Upper Band', line=dict(color='blue')),
                          row=2, col=1)
fig_bb_strategy.add_trace(go.Scatter(x=data['Date'], y=data['BB_Lower'], mode='lines', name='Lower Band', line=dict(color='coral')),
                          row=2, col=1)
fig_bb_strategy.add_trace(go.Scatter(x=data['Date'], y=data['BB_Middle'], mode='lines', name='Middle Band', line=dict(color='lightblue')),
                          row=2, col=1)

# Update layout
fig_bb_strategy.update_layout(height=800, showlegend=False)

# Show the figure
st.plotly_chart(fig_bb_strategy)

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