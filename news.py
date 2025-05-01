import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json
from streamlit_option_menu import option_menu

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="PY NEWS - Enhanced Edition",
    layout="wide",
    page_icon="📰",
    initial_sidebar_state="collapsed"
)

# --- CSS STYLING ---
st.markdown("""
<style>
:root {
    --primary-red: #BB1919;
    --nav-bg: #121212;
    --card-hover: #F8F8F8;
}

[data-testid="stHorizontalBlock"] {
    background: var(--nav-bg);
    padding: 0.5rem 1rem !important;
    border-radius: 0 0 15px 15px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.st-c7 {
    font-weight: 500 !important;
    letter-spacing: 0.5px;
}

[data-testid="stHorizontalBlock"] .st-c7:hover {
    transform: translateY(-2px);
    transition: all 0.2s ease;
}

[data-testid="stHorizontalBlock"] .st-c7[aria-selected="true"] {
    background: var(--primary-red) !important;
    border-radius: 8px !important;
}

.lottie-container {
    margin: -2rem 0 1rem 0;
}

.news-card {
    border-bottom: 1px solid #eee;
    padding: 1.5rem 0;
    transition: all 0.3s ease;
}

.news-card:hover {
    background: var(--card-hover);
    padding-left: 1rem !important;
}

.news-image {
    width: 100%;
    height: 160px;
    object-fit: cover;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    cursor: pointer;
    border: none;
}

.timestamp {
    color: #666;
    font-size: 0.85rem;
    margin: 0.3rem 0;
}

.category-tag {
    background: var(--primary-red);
    color: white !important;
    padding: 0.3rem 0.7rem;
    border-radius: 20px;
    font-size: 0.8rem;
    display: inline-block;
    margin: 0.2rem 0.5rem 0.2rem 0;
}
</style>
""", unsafe_allow_html=True)

# --- SECRETS MANAGEMENT ---
try:
    API_KEY = st.secrets["newsapi_key"]
except:
    st.error("""
        **Configuration Required**  
        Create `.streamlit/secrets.toml` with:  
        ```
        newsapi_key = "YOUR_API_KEY"
        ```
    """)
    st.stop()

# --- TOPIC MAPPING ---
TOPICS = {
    "Headlines": {
        "url": "https://newsapi.org/v2/top-headlines?country=us&pageSize=50",
        "icon": "newspaper"
    },
    "World": {
        "url": "https://newsapi.org/v2/top-headlines?category=general&pageSize=50",
        "icon": "globe-americas"
    },
    "Business": {
        "url": "https://newsapi.org/v2/top-headlines?category=business&pageSize=50",
        "icon": "graph-up"
    },
    "Tech": {
        "url": "https://newsapi.org/v2/everything?domains=techcrunch.com&pageSize=50",
        "icon": "cpu"
    },
    "Health": {
        "url": "https://newsapi.org/v2/top-headlines?category=health&pageSize=50",
        "icon": "heart-pulse"
    },
    "Science": {
        "url": "https://newsapi.org/v2/top-headlines?category=science&pageSize=50",
        "icon": "rocket"
    },
    "Sports": {
        "url": "https://newsapi.org/v2/top-headlines?category=sports&pageSize=50",
        "icon": "trophy"
    },
    "Entertainment": {
        "url": "https://newsapi.org/v2/top-headlines?category=entertainment&pageSize=50",
        "icon": "film"
    },
    "Politics": {
        "url": "https://newsapi.org/v2/everything?q=politics&pageSize=50",
        "icon": "building"
    }
}

# --- NAVBAR ---
selected_topic = option_menu(
    menu_title=None,
    options=list(TOPICS.keys()),
    icons=[TOPICS[t]["icon"] for t in TOPICS],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "0.5rem",
            "background-color": "var(--nav-bg)",
            "border-radius": "0 0 15px 15px"
        },
        "icon": {
            "color": "rgba(255,255,255,0.7)", 
            "font-size": "16px",
            "margin-right": "8px"
        },
        "nav-link": {
            "font-size": "14px",
            "text-align": "left",
            "margin": "0 0.5rem",
            "padding": "0.5rem 1rem",
            "border-radius": "8px",
            "transition": "all 0.2s ease",
            "--hover-color": "rgba(255,255,255,0.1)"
        },
        "nav-link-selected": {
            "background-color": "var(--primary-red)",
            "font-weight": "bold",
            "box-shadow": "0 2px 4px rgba(0,0,0,0.2)"
        },
    },
    key="enhanced-nav"
)

# --- TITLE ABOVE LOTTIE ---
st.markdown("<h1 style='text-align: center; color: var(--primary-red); margin-bottom: 0.5rem;'>PY NEWS</h1>", unsafe_allow_html=True)

# --- LOTTIE ANIMATION ---
def load_lottie(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

st.markdown("<div class='lottie-container'>", unsafe_allow_html=True)
lottie_news = load_lottie("news2.json")
st_lottie(lottie_news, speed=0.5, height=300, loop=True, key="main-lottie")
st.markdown("</div>", unsafe_allow_html=True)

# --- NEWS FETCHER ---
def fetch_news(topic: str):
    try:
        url = f"{TOPICS[topic]['url']}&apiKey={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("articles", [])
    except Exception as e:
        st.error(f"🚨 News fetch error: {str(e)}")
        return []

# --- ARTICLE DISPLAY ---
def display_article(article: dict):
    with st.container():
        col1, col2 = st.columns([1, 3], gap="medium")
        story_url = article.get("url", "#")
        with col1:
            img = article.get("urlToImage", "https://via.placeholder.com/800x450?text=No+Image")
            # Make image clickable using markdown <a> tag
            st.markdown(
                f"<a href='{story_url}' target='_blank'><img class='news-image' src='{img}'></a>",
                unsafe_allow_html=True
            )
        with col2:
            # Metadata
            st.markdown(
                f"<div style='margin-bottom:0.5rem'>"
                f"<span class='category-tag'>{selected_topic}</span>"
                f"<span class='timestamp'>{article.get('publishedAt', '')[:10]}</span>"
                f"</div>",
                unsafe_allow_html=True
            )
            # Title
            title = article.get("title", "Untitled Article")
            st.markdown(
                f"<h3 style='margin:0;padding:0;font-size:1.3rem;'>"
                f"<a href='{story_url}' target='_blank' style='color:inherit;text-decoration:none;'>{title}</a>"
                f"</h3>",
                unsafe_allow_html=True
            )
            # Description
            desc = article.get("description", "No description available")
            st.markdown(
                f"<p style='color:#666;margin:0.5rem 0;line-height:1.5;'>{desc}</p>", 
                unsafe_allow_html=True
            )
            # Author/Source
            author = article.get("author", "Unknown Author")
            source = article.get("source", {}).get("name", "Unknown Source")
            st.markdown(
                f"<div style='color:#888;font-size:0.9rem;margin-top:0.5rem;'>"
                f"📝 {author} | 🏢 {source}"
                f"</div>",
                unsafe_allow_html=True
            )
            # Continue to story button
            st.markdown(
                f"<a href='{story_url}' target='_blank'><button style='background-color: var(--primary-red); color: white; border: none; border-radius: 6px; padding: 0.5rem 1.2rem; margin-top: 0.7rem; cursor: pointer;'>Continue to story</button></a>",
                unsafe_allow_html=True
            )
        st.markdown("<div class='news-card'></div>", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🔍 Search News")
    search_query = st.text_input("Enter keywords:", placeholder="AI, Climate, Elections...")
    if search_query:
        st.info(f"Showing results for: '{search_query}'")
        search_url = f"https://newsapi.org/v2/everything?q={search_query}&apiKey={API_KEY}"
        try:
            articles = requests.get(search_url).json().get("articles", [])
        except:
            articles = fetch_news(selected_topic)
    st.markdown("## 🌐 Top Categories")
    for topic in TOPICS:
        st.button(f"{TOPICS[topic]['icon']} {topic}", use_container_width=True)

# --- MAIN CONTENT ---
st.markdown(f"<h1 style='margin-top:0.5rem;'>{selected_topic} News</h1>", unsafe_allow_html=True)

if not search_query:
    articles = fetch_news(selected_topic)

if articles:
    for article in articles[:25]:
        display_article(article)
else:
    st.warning("No articles found. Try another topic or search term.")

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#666;padding:2rem;font-size:0.9rem;'>"
    "📰 Powered by NewsAPI | 🚀 Enhanced Streamlit Design"
    "</div>", 
    unsafe_allow_html=True
)
