import streamlit as st 
from streamlit.components.v1 import html

import json 
import requests 
from streamlit_lottie import st_lottie 

st.set_page_config(
    page_title = "Poder - Home",
    page_icon="🪙"
)

url = requests.get( 
    "https://lottie.host/2bad34a1-efda-4626-bc5c-e2619a2cd42f/rHOi6OSkx4.json")

url_json = dict() 
  
if url.status_code == 200: 
    url_json = url.json() 
else: 
    print("Error in the URL") 

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

def main():
    # st.title("Poder: Empowering Your Financial Journey")
    st.markdown("<h1 style='font-size:2.3em;','font-family: Arial, sans-serif;'>Poder: Empowering Your Financial Journey</h1>", unsafe_allow_html=True)
    st_lottie(url_json)
    
    st.write("""
    <p style='text-align: justify;'>
        <strong>Poder</strong> is a Spanish word that translates to power or to be able to in English. The aim of Poder is to empower individuals to take control of their financial lives, make informed decisions, and navigate their financial journey with confidence. Delve into different <strong>Investment Strategies</strong> , learn about <strong>Technical Analysis</strong> and we hope that you have a great experince.
    </p>
    <p>
        Happy Podering!!!
    </p>
""", unsafe_allow_html=True)

    # Create an empty space in the middle to center-align the buttons
    # st.markdown("""<style>div.stButton > button:first-child {background-color: blue;}</style>""", unsafe_allow_html=True)


    if st.button("Explore Technical Analysis"):
            nav_page("Technical_Analysis")


if __name__ == "__main__":
    main()