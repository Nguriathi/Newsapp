from optparse import Option
from unicodedata import category
from unittest import result
import streamlit as st
import requests
#import pycountry
from newsapi import api
from streamlit_lottie import st_lottie
import json
from streamlit_option_menu import option_menu


st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center; color:red;'>PY NEWS</h1>", unsafe_allow_html=True)

selected = option_menu(
                menu_title=None,  # required
                options=["Headlines", "Technology", "Trump", "Crypto"],  
                icons=["🌎", "🌎", "🌎", "🌎"],  
                #menu_icon="cast",  
                default_index=0,  
                orientation="horizontal",
                styles={
                    "container": {"padding": "0px", "background-color": "#2C3333"},
                    "icon": {"color": "orange", "font-size": "15px"},
                    "nav-link": {
                        "font-size": "15px",
                        "text-align": "center",
                        "margin": "0.5px",
                        "--hover-color": "red",
                    },
                    "nav-link-selected": {"background-color": "red"},
                },
            )

def load_lottiefile(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)


lottie_news = load_lottiefile("news2.json")
st_lottie(
        lottie_news,
        speed=0.5,
        reverse=False,
        loop=True,
        height=500,
        width=None,
        key=None,
     )


if selected == "Headlines":
    
    url = f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={api}"


    r = requests.get(url)
    r = r.json()

    articles = r['articles']
    for article in articles:
        st.header(article['title'])
        #.........st.write(article['publishedAt'])
        st.markdown(f"<span style ='background-color:red; padding:10px; border-radius:20px;'> Published at: {article['publishedAt']}</span>", unsafe_allow_html=True)
       
        if article['author']:
            st.write(article['author'])

        st.write(article['source']['name'])
        st.write(article['description'])
        st.image(article['urlToImage'])



if selected == "Crypto":
    url = f"https://newsapi.org/v2/everything?q=bitcoin&apiKey={api}"


    r = requests.get(url)
    r = r.json()

    articles = r['articles']
    for article in articles:
        st.header(article['title'])
        #.........st.write(article['publishedAt'])
        st.markdown(f"<span style ='background-color:red; padding:10px; border-radius:20px;'> Published at: {article['publishedAt']}</span>", unsafe_allow_html=True)
       
        if article['author']:
            st.write(article['author'])

        st.write(article['source']['name'])
        st.write(article['description'])
        st.image(article['urlToImage'])

if selected == "Technology":
    url = f"https://newsapi.org/v2/everything?domains=techcrunch.com,thenextweb.com&apiKey={api}"

    r = requests.get(url)
    r = r.json()

    articles = r['articles']
    for article in articles:
        st.header(article['title'])
        #.........st.write(article['publishedAt'])
        st.markdown(f"<span style ='background-color:red; padding:10px; border-radius:20px;'> Published at: {article['publishedAt']}</span>", unsafe_allow_html=True)
       
        if article['author']:
            st.write(article['author'])

        st.write(article['source']['name'])
        st.write(article['description'])
        st.image(article['urlToImage'])

if selected == "Trump":
    url = f"https://newsapi.org/v2/top-headlines?q=trump&apiKey={api}"


    r = requests.get(url)
    r = r.json()

    articles = r['articles']
    for article in articles:
        st.header(article['title'])
        #.........st.write(article['publishedAt'])
        st.markdown(f"<span style ='background-color:red; padding:10px; border-radius:20px;'> Published at: {article['publishedAt']}</span>", unsafe_allow_html=True)
       
        if article['author']:
            st.write(article['author'])

        st.write(article['source']['name'])
        st.write(article['description'])
        st.image(article['urlToImage'])

#else:
   # st.warning('No option is selected')

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
