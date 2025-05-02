import streamlit as st
import requests
import json
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="PY NEWS",
    layout="wide",
    page_icon="📰"
)

# --- CSS STYLING ---
st.markdown("""
<style>
:root {
    --primary-red: #BB1919;
    --nav-bg: #121212;
    --card-hover: #F8F8F8;
    --text-color: #EEE;
}
body {
    background-color: #181818;
    color: var(--text-color);
}
.pynews-title {
    text-align: center;
    color: var(--primary-red);
    margin-bottom: 0.7rem;
    margin-top: 0.7rem;
    font-size: 2.5rem;
    font-weight: 900;
    letter-spacing: 2px;
}
.stHorizontalBlock {
    min-width: 600px;
}
@media (max-width: 900px) {
    .stHorizontalBlock {
        min-width: 400px;
    }
}
@media (max-width: 600px) {
    .stHorizontalBlock {
        min-width: 300px;
    }
    .pynews-title {
        font-size: 1.5rem;
    }
}
.lottie-container {
    margin-bottom: 2rem;
}
.news-card {
    border-bottom: 1px solid #222;
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
    color: #999;
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
a {
    color: inherit;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
button.continue-btn {
    background-color: var(--primary-red);
    color: white;
    border: none;
    border-radius: 6px;
    padding: 0.5rem 1.2rem;
    margin-top: 0.7rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
button.continue-btn:hover {
    background-color: #a11515;
}

/* Search input with left icon */
.stTextInput > div > div {
    position: relative;
}
.stTextInput > div > div > input {
    background-color: #222 !important;
    color: #eee !important;
    border-radius: 20px;
    border: 1px solid #444;
    padding-left: 3.0rem !important; /* Increased padding for icon */
}
/* Icon inside input */
.stTextInput > div > div::before {
    content: '🔍'; /* Generic search symbol */
    position: absolute;
    left: 10px;
    top: 50%;
    transform: translateY(-50%);
    color: rgba(255,255,255,0.7); /* Matches navbar icon color */
    font-size: 1.2rem;
    pointer-events: none;
}
</style>
""", unsafe_allow_html=True)

# --- SECRETS MANAGEMENT ---
try:
    API_KEY = st.secrets["newsapi_key"]
except Exception:
    st.error("""
        **Configuration Required**  
        Create `.streamlit/secrets.toml` with:  
        ```
        newsapi_key = "YOUR_API_KEY"
        ```
        Get your API key from https://newsapi.org/
    """)
    st.stop()

# --- TOPIC MAPPING ---
TOPICS = {
    "Headlines": {"url": "https://newsapi.org/v2/top-headlines?country=us&pageSize=50", "icon": "newspaper"},
    "World": {"url": "https://newsapi.org/v2/top-headlines?category=general&pageSize=50", "icon": "globe-americas"},
    "Business": {"url": "https://newsapi.org/v2/top-headlines?category=business&pageSize=50", "icon": "graph-up"},
    "Tech": {"url": "https://newsapi.org/v2/everything?domains=techcrunch.com&pageSize=50", "icon": "cpu"},
    "Health": {"url": "https://newsapi.org/v2/top-headlines?category=health&pageSize=50", "icon": "heart-pulse"},
    "Science": {"url": "https://newsapi.org/v2/top-headlines?category=science&pageSize=50", "icon": "rocket"},
    "Sports": {"url": "https://newsapi.org/v2/top-headlines?category=sports&pageSize=50", "icon": "trophy"},
    "Entertainment": {"url": "https://newsapi.org/v2/top-headlines?category=entertainment&pageSize=50", "icon": "film"},
    "Politics": {"url": "https://newsapi.org/v2/everything?q=politics&pageSize=50", "icon": "building"},
}

# --- SESSION STATE ---
if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = "Headlines"
if "search_query" not in st.session_state:
    st.session_state.search_query = ""

# --- TITLE ---
st.markdown('<div class="pynews-title">PY NEWS</div>', unsafe_allow_html=True)

# --- NAVBAR ---
selected_topic = option_menu(
    menu_title=None,
    options=list(TOPICS.keys()),
    icons=[TOPICS[t]["icon"] for t in TOPICS],
    default_index=list(TOPICS.keys()).index(st.session_state.selected_topic),
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
st.session_state.selected_topic = selected_topic

# --- SEARCH BAR (below navbar) ---
search_query = st.text_input(
    "Search news",
    value=st.session_state.search_query,
    placeholder="Type keywords and press Enter (e.g. AI, Elections, SpaceX...)",
    label_visibility="collapsed"
)
st.session_state.search_query = search_query.strip()

# --- LOTTIE ANIMATION (below search bar) ---
def load_lottie(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
st.markdown('<div class="lottie-container">', unsafe_allow_html=True)
lottie_news = load_lottie("news2.json")
st_lottie(lottie_news, speed=0.5, height=300, loop=True, key="main-lottie")
st.markdown('</div>', unsafe_allow_html=True)

# --- NEWS FETCHER ---
def fetch_news(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("articles", [])
    except Exception as e:
        st.error(f"🚨 News fetch error: {str(e)}")
        return []

# --- ARTICLE DISPLAY ---
def display_article(article: dict, topic: str):
    with st.container():
        col1, col2 = st.columns([1, 3], gap="medium")
        story_url = article.get("url", "#")
        with col1:
            img = article.get("urlToImage", "https://via.placeholder.com/800x450?text=No+Image")
            st.markdown(
                f"<a href='{story_url}' target='_blank' rel='noopener noreferrer'><img class='news-image' src='{img}' alt='Article image'></a>",
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f"<div style='margin-bottom:0.5rem'>"
                f"<span class='category-tag'>{topic}</span>"
                f"<span class='timestamp'>{article.get('publishedAt', '')[:10]}</span>"
                f"</div>",
                unsafe_allow_html=True
            )
            title = article.get("title", "Untitled Article")
            st.markdown(
                f"<h3 style='margin:0;padding:0;font-size:1.3rem;'>"
                f"<a href='{story_url}' target='_blank' rel='noopener noreferrer' style='color:inherit;text-decoration:none;'>{title}</a>"
                f"</h3>",
                unsafe_allow_html=True
            )
            desc = article.get("description", "No description available")
            st.markdown(
                f"<p style='color:#666;margin:0.5rem 0;line-height:1.5;'>{desc}</p>",
                unsafe_allow_html=True
            )
            author = article.get("author", "Unknown Author")
            source = article.get("source", {}).get("name", "Unknown Source")
            st.markdown(
                f"<div style='color:#888;font-size:0.9rem;margin-top:0.5rem;'>"
                f"📝 {author} | 🏢 {source}"
                f"</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<a href='{story_url}' target='_blank' rel='noopener noreferrer'><button class='continue-btn'>Continue to story</button></a>",
                unsafe_allow_html=True
            )
        st.markdown("<div class='news-card'></div>", unsafe_allow_html=True)

# --- MAIN CONTENT ---
if st.session_state.search_query:
    url = f"https://newsapi.org/v2/everything?q={st.session_state.search_query}&pageSize=25&apiKey={API_KEY}"
    articles = fetch_news(url)
    title_text = f"Search Results for '{st.session_state.search_query}'"
else:
    url = f"{TOPICS[st.session_state.selected_topic]['url']}&apiKey={API_KEY}"
    articles = fetch_news(url)
    title_text = f"{st.session_state.selected_topic} News"

st.markdown(f"<h2 style='margin-top:1rem; color: var(--primary-red); text-align:center'>{title_text}</h2>", unsafe_allow_html=True)

if articles:
    for article in articles[:25]:
        display_article(article, st.session_state.selected_topic)
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
