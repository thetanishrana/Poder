import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from prophet import Prophet
from datetime import datetime, timedelta
import pandas as pd

# Function to fetch historical stock data
def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# Function to plot Ichimoku Cloud
def plot_ichimoku(stock_data):
    fig = go.Figure()

    # Plotting closing prices
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Closing Price'))

    # Calculating Ichimoku Cloud components
    conversion_line = stock_data['Close'].rolling(window=9).mean()
    base_line = stock_data['Close'].rolling(window=26).mean()
    lead_span_a = (conversion_line + base_line) / 2
    lead_span_b = stock_data['Close'].rolling(window=52).mean()
    
    # Plotting Ichimoku Cloud
    fig.add_trace(go.Scatter(x=stock_data.index, y=lead_span_a, mode='lines', name='Ichimoku Cloud A', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=stock_data.index, y=lead_span_b, mode='lines', name='Ichimoku Cloud B', line=dict(color='red')))
    
    fig.update_layout(title=f'{ticker} Stock Price Forecast with Ichimoku Cloud',
                      xaxis_title='Date',
                      yaxis_title='Stock Price (USD)',
                      xaxis_rangeslider_visible=True)

    return fig

# Function to forecast stock prices using Prophet
def forecast_stock_prices(stock_data, years_to_forecast):
    df_prophet = stock_data.reset_index()[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})

    # Create and fit the model
    model = Prophet()
    model.fit(df_prophet)

    # Create a dataframe with future dates for forecasting
    future = model.make_future_dataframe(periods=365 * years_to_forecast)  # Forecasting for the selected number of years
    forecast = model.predict(future)

    # Plot the forecast
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Actual Prices'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecasted Prices'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], fill=None, mode='lines', line=dict(color='gray'), name='Lower Bound'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], fill='tonexty', mode='lines', line=dict(color='gray'), name='Upper Bound'))

    fig.update_layout(title=f'{ticker} Stock Price Forecast for {years_to_forecast} Years with Prophet',
                      xaxis_title='Date',
                      yaxis_title='Stock Price (USD)',
                      xaxis_rangeslider_visible=True)

    return fig

# Streamlit app
st.title('Stock Price Forecasting using Ichimoku Cloud Analysis')

# Create an expander
with st.expander("Want to Learn about Ichimoku Cloud Analysis?"):
    # Content inside the expander
    st.subheader("Ichimoku Cloud Analysis")
    st.write("""
    <p style='text-align: justify;'>
        The first analysis performed is the Ichimoku Cloud analysis. The Ichimoku Cloud is a technical analysis indicator that provides insights into the potential future direction of the stock price. Here's how the Ichimoku Cloud components are calculated and plotted:
    </p>
""", unsafe_allow_html=True)
    st.write("""
    <ul style='text-align: justify;'>
        <li><strong>Closing Prices:</strong> The closing prices of the stock are plotted over time.</li> 
    </ul>
""", unsafe_allow_html=True)
    st.write("""
    <ul style='text-align: justify;'>
        <li><strong>Conversion Line (Tenkan-sen):</strong> A 9-period simple moving average of closing prices.</li> 
    </ul>
""", unsafe_allow_html=True)
    st.write("""
    <ul style='text-align: justify;'>
        <li><strong>Base Line (Kijun-sen):</strong> A 26-period simple moving average of closing prices.</li> 
    </ul>
""", unsafe_allow_html=True)
    st.write("""
    <ul style='text-align: justify;'>
        <li><strong>Lead Span A (Senkou Span A):</strong> The average of the Conversion Line and the Base Line, plotted 26 periods ahead.</li> 
    </ul>
""", unsafe_allow_html=True)
    st.write("""
    <ul style='text-align: justify;'>
        <li><strong>ead Span B (Senkou Span B):</strong> A 52-period simple moving average of closing prices, plotted 26 periods ahead.</li> 
    </ul>
""", unsafe_allow_html=True)
    st.write("""
    <p style='text-align: justify;'>
        The Ichimoku Cloud is formed by shading the region between Lead Span A and Lead Span B. This cloud helps traders identify potential support and resistance levels, as well as trend direction.


    </p>
""", unsafe_allow_html=True)

# User input for the stock ticker
ticker = st.text_input('Enter the stock symbol (e.g., AAPL):', 'AAPL')

# User input for the number of years to consider
years_to_consider = st.slider('Select the number of years to consider for historical data:', 1, 10, 5)

# Calculate start and end dates based on user input
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=365 * years_to_consider)).strftime('%Y-%m-%d')

# Fetch historical stock data
stock_data = get_stock_data(ticker, start_date, end_date)

# Calculate Year-to-Date (YTD) Growth
ytd_growth = (stock_data['Close'][-1] / stock_data['Close'].iloc[0] - 1) * 100

# Display YTD Growth Metric
st.metric("YTD Growth", f"{ytd_growth:.2f}%", f"{ticker} YTD Growth")

st.divider()

# Display Ichimoku Cloud
ichimoku_fig = plot_ichimoku(stock_data)
st.plotly_chart(ichimoku_fig)

# User input for the number of years to forecast
years_to_forecast = st.slider('Select the number of years to forecast:', 1, 5, 1)

# Display Prophet Forecast
st.subheader('Forecasting')
prophet_fig = forecast_stock_prices(stock_data, years_to_forecast)
st.plotly_chart(prophet_fig)