import streamlit as st 
from streamlit.components.v1 import html
# import lottie
import numpy as np
# from streamlit.components.v1 import html
import json 
import requests 
from streamlit_lottie import st_lottie 


# Function to resize Lottie animation
# def resize_lottie_animation(lottie_json, width, height, scale_factor=0.5):
#     lottie_data = json.loads(lottie_json)

#     # Resize the animation with scale factor
#     lottie_data['w'] = int(lottie_data['w'] * scale_factor)
#     lottie_data['h'] = int(lottie_data['h'] * scale_factor)

#     resized_lottie_json = json.dumps(lottie_data)
#     return resized_lottie_json

url = requests.get( 
    "https://lottie.host/43f83282-3ceb-472f-8f6f-893b8761e10a/XCYDFiFeI2.json")

url1= requests.get(
    "https://lottie.host/ffc2c93e-e338-4028-8668-aab1c8399961/gnPY2YcETf.json"
)
url2= requests.get(
    "https://lottie.host/b6eda197-53d3-4c06-8667-a977f33ef7f5/HeE5KNQ1S0.json"
)
url3= requests.get(
    "https://lottie.host/802063cd-172c-4d6b-ac74-f583c5ff44b3/txo8Xx4kzo.json"
)
url4= requests.get(
    "https://lottie.host/2f88498c-cce2-477a-a216-e717a84f1dbd/d517dA2LRw.json"
)

url_json = dict() 
ur11_json = dict()
ur12_json = dict()
url3_json = dict()
url4_json = dict()

  
if url.status_code == 200: 
    url_json = url.json() 
else: 
    print("Error in the URL") 
    
if url1.status_code == 200: 
    url1_json = url1.json() 
else: 
    print("Error in the URL") 
    
if url2.status_code == 200: 
    url2_json = url2.json() 
else: 
    print("Error in the URL") 
    
if url3.status_code == 200: 
    url3_json = url3.json() 
else: 
    print("Error in the URL") 

if url4.status_code == 200: 
    url4_json = url4.json() 
else: 
    print("Error in the URL") 

st.set_page_config(
    page_title = "Technical Analysis",
    page_icon="💹"
)


# scale_factor = 0.5

# st.title("Technical Analysis")

# st_lottie(resize_lottie_animation(url_json, 400, 300, scale_factor))
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

st.title("Technical Analysis")

st_lottie(url_json)

st.subheader("What is Technical Analysis?")
st.write("""
    <p style='text-align: justify;'>
    1. Technical analysis is a <strong>trading discipline</strong> employed to evaluate investments and identify trading opportunities in price trends and patterns seen on charts.
    </p>
""", unsafe_allow_html=True)
st.write("""
    <p style='text-align: justify;'>
    2. Do not confuse it with fundamnetal analysis.Unlike fundamental analysis, which attempts to evaluate a security's value based on business results such as sales and earnings, technical analysis <strong>focuses on the study of price and volume</strong>.
    </p>
""", unsafe_allow_html=True)


st.subheader("Why is technical analysis used?")
st.write("""
    <p style='text-align: justify;'>
    1. Technical analysis tools are used to scrutinize the ways supply and demand for a security will affect changes in price, volume, and implied volatility. It operates from the assumption that past trading activity and price changes of a security can be valuable indicators of the security's future price movements when paired with appropriate investing or trading rules.
    </p>
""", unsafe_allow_html=True)
st.write("""
    <p style='text-align: justify;'>
    2. It is often used to generate short-term trading signals from various charting tools, but can also help improve the evaluation of a security's strength or weakness relative to the broader market or one of its sectors. This information helps analysts improve their overall valuation estimate.
    </p>
""", unsafe_allow_html=True)

st.subheader("Who can benefit from doing Technical Analysis?")
st.write("""
    <p style='text-align: justify;'>
    1. Technical analysis is employed by a diverse array of market participants, including individual traders, institutional investors, day traders, and financial analysts. It involves analyzing historical price charts, patterns, and technical indicators to make predictions about future price movements. Individual traders often use technical analysis to identify trends and entry/exit points, while institutional investors integrate it with fundamental analysis for a comprehensive market view. Day traders heavily rely on short-term technical signals for quick decision-making
    </p>
""", unsafe_allow_html=True)
st.write("""
    <p style='text-align: justify;'>
    2. While technical analysis has its critics, particularly regarding its theoretical basis and potential for subjectivity, many market participants find it a valuable tool for understanding market sentiment and making informed trading decisions.
    </p>
""", unsafe_allow_html=True)



st.divider()

st.header("Strategies used in Technical Analysis:")
st_lottie(url1_json)
st.markdown("1.**Moving Averages:** ")
st.write("""
    <p style='text-align: justify;'>
    <strong>Simple Moving Average (SMA)</strong>: Average price over a specified period.\n
    <strong>Exponential Moving Average (EMA)</strong>: Gives more weight to recent prices.
    </p>
""", unsafe_allow_html=True)

st.markdown("2.**Relative Strength Index (RSI):** ")
st.write("""
    <p style='text-align: justify;'>
    Measures the speed and change of price movements.\n
    RSI values above 70 indicate overbought conditions, and values below 30 suggest oversold conditions.
    </p>
""", unsafe_allow_html=True)

st.markdown(" 3.**Bollinger Bands:**")
st.write("""
    <p style='text-align: justify;'>
    Consists of a middle band (SMA) and upper/lower bands based on volatility.\n
    Helps identify overbought or oversold conditions.
    </p>
""", unsafe_allow_html=True)

st.markdown(" 4.**MACD (Moving Average Convergence Divergence):**")
st.write("""
    <p style='text-align: justify;'>
    Consists of two moving averages and a histogram.\n
    Signal line crossovers and histogram patterns are used for trend confirmation.
    </p>
""", unsafe_allow_html=True)

if st.button("Learn More about Strategy"):
    nav_page("Strategy")

st.divider()

st.header("Introduction to Time Series Analysis")
st_lottie(url2_json)
st.write("""
    <p style='text-align: justify;'>
        A time series is a collection of data points or observations collected, recorded, or measured over successive,
        evenly spaced intervals of time. It's a powerful tool for analyzing temporal patterns and making predictions.
    </p>
""", unsafe_allow_html=True)

st.subheader("Key Concepts")
st.write("""
    <p style='text-align: justify;'>
        1.<strong>Sequential Order:</strong> Time series data is organized in chronological order, with each data point corresponding to a specific moment in time.
    </p>
""", unsafe_allow_html=True)
st.write("""
    <p style='text-align: justify;'>
        2<strong>Time as an Independent Variable:</strong> Unlike other types of data, time series data has a natural temporal ordering, making time an essential independent variable.
    </p>
""", unsafe_allow_html=True)
st.write("""
    <p style='text-align: justify;'>
        3.<strong>Examples of Time Series Data:</strong> Examples include stock prices over days, monthly sales figures, hourly temperature readings, or daily website traffic.
    </p>
""", unsafe_allow_html=True)


st.subheader("Components of Time Series")
st.write("""
    <p style='text-align: justify;'>
        1.<strong>Trend:</strong> The long-term movement or direction in the data. A trend may be upward (increasing), downward (decreasing), or stable..
    </p>
""", unsafe_allow_html=True)
st.write("""
    <p style='text-align: justify;'>
        2.<strong>Seasonality:</strong>  Repeating patterns that occur at regular intervals, often related to a specific season, day of the week, or time of day.
    </p>
""", unsafe_allow_html=True)
st.write("""
    <p style='text-align: justify;'>
        3.<strong>Cyclic Patterns:</strong> Repeating patterns that are not strictly tied to a fixed time frame but occur over a more extended period.
    </p>
""", unsafe_allow_html=True)
st.write("""
    <p style='text-align: justify;'>
        4.<strong>Random Fluctuations:</strong> Unpredictable variations or noise in the data that don't follow a specific pattern.
    </p>
""", unsafe_allow_html=True)

st.subheader("Applications of Time Series Analysis")
st.write("""
    <p style='text-align: justify;'>
    1.<strong>Economics and Finance:</strong> Analyzing economic indicators, stock prices, and financial market trends.
    </p>
""", unsafe_allow_html=True)
st.write("""
    <p style='text-align: justify;'>
        2.<strong>Meteorology:</strong> Forecasting weather patterns and temperature variations.
    </p>
""", unsafe_allow_html=True)
st.write("""
    <p style='text-align: justify;'>
        3.<strong>Healthcare:</strong> Monitoring patient vital signs over time or tracking disease prevalence.
    </p>
""", unsafe_allow_html=True)
st.write("""
    <p style='text-align: justify;'>
        4.<strong>Operations and Business:</strong> Managing inventory levels, analyzing sales patterns, and predicting demand.
    </p>
""", unsafe_allow_html=True)

st.subheader("Importance of Time Series Analysis")
st.write("""
    <p style='text-align: justify;'>
        1.<strong>Predictive Analytics:</strong> Time series analysis enables forecasting future values based on historical patterns, aiding in decision-making.
    </p>
""", unsafe_allow_html=True)
st.write("""
    <p style='text-align: justify;'>
        2.<strong>Pattern Recognition:</strong> Identifying trends, seasonality, and anomalies helps in understanding underlying patterns within the data.
    </p>
""", unsafe_allow_html=True)
st.write("""
    <p style='text-align: justify;'>
        3.<strong>Optimization:</strong> Businesses can optimize operations, inventory, and resource allocation based on insights gained from time series analysis.
    </p>
""", unsafe_allow_html=True)
st.write("""
    <p style='text-align: justify;'>
        4.<strong>Risk Management:</strong> Assessing and mitigating risks by anticipating potential fluctuations or disruption
    </p>
""", unsafe_allow_html=True)

if st.button("See Forecasting in action!!!"):
    nav_page("Forecast")

st.divider()


st.header("Poder Chatbot")
st_lottie(url3_json)
st.write("""
    <p style='text-align: justify;'>
        Imagine having a financial chatbot as your dedicated guide through the intricacies of personal finance. As you start your journey, the chatbot warmly welcomes you and gathers essential information about your financial goals and interests. The chatbot becomes your personalized tutor, offering bite-sized lessons on budgeting, saving, investing, and more. 
    </p>
""", unsafe_allow_html=True)
st.write("""
    <p style='text-align: justify;'>
        It tailors learning paths based on your preferences, providing quizzes for reinforcement and instant feedback. Whether you're setting financial goals, creating budgets, or delving into investment strategies, the chatbot is there every step of the way, offering insights, answering questions, and celebrating your achievements. 
    </p>
""", unsafe_allow_html=True)
st.write("""
    <p style='text-align: justify;'>
        With continuous updates on market trends and personalized advice, this chatbot transforms financial education into an interactive and accessible experience, empowering you to make informed decisions and progress confidently in your financial journey.
    </p>
""", unsafe_allow_html=True)

if st.button("Chat with Matt"):
    nav_page("Chat_with_Matt")

st.divider()

st.header("Roadmap")
st_lottie(url4_json)
st.write("""
    <p style='text-align: justify;'>
        We have also curated a roadmap especially for you, to help you along your financial journey. This roadmap is meant to provide a overview for the individual to use as a foundation for their strategies and goals.
    </p>
""", unsafe_allow_html=True)

if st.button("Roadmap"):
    nav_page("Roadmap")