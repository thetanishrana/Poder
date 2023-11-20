import streamlit as st
from datetime import date
import time

import numpy as np
import pandas as pd

import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
from streamlit.components.v1 import html

# Page configurations
st.set_page_config(
    page_title="Poder - Strategy",
    page_icon="🪙"
)

st.title('Strategies')

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

tab1, tab2, tab3 = st.tabs(["SMA", "MACD", "BB"])

with tab1:
    st.header("Simple Moving Average Method")
    st.write("""
    <p style='text-align: justify;'>
        <strong>A Simple Moving Average (SMA)</strong> is a commonly used technical indicator in financial markets to smooth out price data over a specified time period. 
        It is calculated by taking the average of a set of prices over that period, with the "simple" indicating that each data point is equally weighted in the calculation.
    </p>

    <p style='text-align: justify;'>
        One common strategy for generating buying and selling signals using the Simple Moving Average is based on the crossover of short-term and long-term moving averages. 
        The two main types of moving averages involved in this strategy are:
    </p>

    <ul style='text-align: justify;'>
        <li><strong>Short-term SMA (Fast Moving Average):</strong> This is calculated over a shorter time period and is more responsive to recent price changes.</li>
        <li><strong>Long-term SMA (Slow Moving Average):</strong> This is calculated over a longer time period and provides a smoother trend, being less responsive to short-term price fluctuations.</li>
    </ul>

    <p style='text-align: justify;'>
        The basic idea is that when the short-term SMA crosses above the long-term SMA, it may be considered a bullish signal or a "buy" signal, suggesting that the trend is turning upward. 
        Conversely, when the short-term SMA crosses below the long-term SMA, it may be considered a bearish signal or a "sell" signal, suggesting that the trend is turning downward.
    </p>
""", unsafe_allow_html=True)

    if st.button("See SMA in action 📈"):
        nav_page("Try_SMA")


with tab2:
    st.header("Moving Average Convergence Divergence")
    st.write("""
    <p style='text-align: justify;'>
        <strong>The Moving Average Convergence Divergence (MACD)</strong> is another popular technical indicator that helps identify potential trends and generate buy/sell signals. The MACD consists of two main components: the MACD line and the Signal line.
    </p>

    <p style='text-align: justify;'>
        Here's a simple explanation of the MACD strategy:
    </p>

    <ul style='text-align: justify;'>
        <li><strong>MACD Line (Fast Line):</strong> This is the difference between two Exponential Moving Averages (EMAs). The commonly used time periods for these EMAs are 12 periods (short-term) and 26 periods (long-term). The MACD line is calculated as follows:</li>
        
    </ul>
""", unsafe_allow_html=True)
    st.latex("MACD Line=12-day EMA−26-day EMA")

    st.write("""
    <ul style='text-align: justify;'>
        <li><strong>Signal Line (Slow Line):</strong> This is a 9-period EMA of the MACD line. It helps smooth out the MACD line and generate trading signals. The Signal line is calculated as follows:</li> 
    </ul>
""", unsafe_allow_html=True)
    st.latex("Signal Line=9-day EMA of MACD Line")

    st.write("""
    <ul style='text-align: justify;'>
        <li><strong>ACD Histogram:</strong> This is the difference between the MACD line and the Signal line. It represents the distance between the MACD line and the Signal line and is often used to identify changes in momentum.</li> 
    </ul>
""", unsafe_allow_html=True)
    st.latex("MACD Histogram=MACD Line−Signal Line")

    st.write("""
    <p style='text-align: justify;'>
        The basic idea is that when the short-term SMA crosses above the long-term SMA, it may be considered a bullish signal or a "buy" signal, suggesting that the trend is turning upward. 
        Conversely, when the short-term SMA crosses below the long-term SMA, it may be considered a bearish signal or a "sell" signal, suggesting that the trend is turning downward.
    </p>
""", unsafe_allow_html=True)

    st.write("""
    <p style='text-align: justify;'>
        Now, let's consider a simple MACD strategy based on the crossover of the MACD line and the Signal line:
    </p>

    <ul style='text-align: justify;'>
        <li><strong>Buy Signal:</strong> When the MACD line crosses above the Signal line.</li> 
    </ul>

    <ul style='text-align: justify;'>
        <li><strong>Sell Signal:</strong> When the MACD line crosses below the Signal line.</li> 
    </ul>
""", unsafe_allow_html=True)

    if st.button("See MACD in action📈"):
        nav_page("Try_MACD")

with tab3:
    st.header("Bollinger Bands")
    st.write("""
    <p style='text-align: justify'>
        <strong>Bollinger Bands</strong> are a technical analysis tool that consists of a middle band being an N-period simple moving average (SMA) and two outer bands that are a specified number of standard deviations away from the middle band. The standard settings typically use a 20-period SMA and two standard deviations.
    </p>

    <p>
        Here's a simple explanation of a Bollinger Bands strategy:
    </p>

    <ul style='text-align: justify;'>
        <li><strong>Middle Band (SMA):</strong> Calculate the N-period simple moving average (SMA) of the closing prices. The commonly used period is 20.</li>
    </ul>
""", unsafe_allow_html=True)
    st.latex("Middle Band (SMA)=20-day SMA of Closing Prices")

    st.write("""
    <ul style='text-align: justify;'>
        <li><strong>Upper Band:</strong> Calculate the upper band by adding two times the standard deviation of the closing prices to the middle band.</li> 
    </ul>
""", unsafe_allow_html=True)
    st.latex("Upper Band=Middle Band (SMA)+2×Standard Deviation of Closing Prices")

    st.write("""
    <ul style='text-align: justify;'>
        <li><strong>Lower Band:</strong> Calculate the lower band by subtracting two times the standard deviation of the closing prices from the middle band.</li> 
    </ul>
""", unsafe_allow_html=True)
    st.latex("Lower Band=Middle Band (SMA)−2×Standard Deviation of Closing Prices")

    st.write("""
    <ul style='text-align: justify;'>
        <li><strong>Bollinger Band Width:</strong> The bandwidth is the difference between the upper and lower bands. It is often used as an indicator of volatility.</li> 
    </ul>
""", unsafe_allow_html=True)
    st.latex("Bollinger Band Width=Upper Band−Lower Band")

    st.write("""
    <p style='text-align: justify'>
        A buy signal is generated when the closing price crosses below the lower Bollinger Band, indicating potential oversold conditions. This suggests that the price has fallen below its historical average, signaling an opportunity for a reversal or bounce back. Conversely, a sell signal occurs when the closing price crosses above the upper Bollinger Band, signaling potential overbought conditions. This indicates that the price has risen above its historical average, suggesting a potential correction or pullback. Traders often interpret these signals as opportunities to enter or exit positions, although it's crucial to consider additional factors and conduct comprehensive analysis to make well-informed trading decisions. Bollinger Bands provide a valuable framework for understanding price dynamics and identifying potential trend reversals in financial markets.
    </p>
""", unsafe_allow_html=True)

    if st.button("See Bollinger Bands in action📈"):
        nav_page("Try_Bollinger_Bands")

