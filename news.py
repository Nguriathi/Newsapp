import streamlit as st
import requests
import logging
from streamlit_lottie import st_lottie
import json
from streamlit_option_menu import option_menu

# --- CONFIGURATION ---
logging.basicConfig(filename='news_app.log', level=logging.ERROR)
st.set_page_config(
    page_title="PY NEWS - Pro Edition",
    layout="wide",
    page_icon="📰",
    initial_sidebar_state="collapsed"
)

# --- EMBEDDED CSS ---
st.markdown("""
<style>
:root {
    --primary-red: #FF4B4B;
    --nav-bg: #1E1E1E;
    --card-bg: #FFFFFF;
    --text-dark: #2C3333;
    --text-light: #F4F4F4;
}

/* Main title */
.main-title {
    color: var(--primary-red) !important;
    text-align: center;
    margin: 1rem 0 0.5rem !important;
    font-size: 3rem !important;
}

/* Category headers */
.category-title {
    color: var(--text-dark);
    margin: 1.5rem 0 !important;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--primary-red);
}

/* News images */
.news-image {
    width: 100%;
    height: 180px;
    object-fit: cover;
    border-radius: 8px;
    transition: transform 0.2s ease;
}

.news-image:hover {
    transform: scale(1.02);
}

/* Article metadata */
.metadata {
    margin-bottom: 0.75rem;
}

.category-tag {
    background: var(--primary-red);
    color: white !important;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    margin-right: 0.5rem;
}

.timestamp {
    color: #666;
    font-size: 0.85rem;
}

/* Article content */
.article-title {
    margin: 0 !important;
    font-size: 1.4rem !important;
}

.article-title a {
    color: inherit !important;
    text-decoration: none !important;
}

.article-desc {
    color: #444;
    margin: 0.5rem 0 !important;
    line-height: 1.6 !important;
}

.article-meta {
    color: #666;
    font-size: 0.9rem;
    margin: 0.75rem 0;
}

/* Story button */
.story-button {
    display: inline-block;
    background: var(--primary-red);
    color: white !important;
    padding: 0.5rem 1.5rem;
    border-radius: 25px;
    text-decoration: none !important;
    transition: all 0.2s ease;
    margin: 1rem 0;
}

.story-button:hover {
    opacity: 0.9;
    transform: translateY(-1px);
}

/* Navbar styling */
[data-testid="stHorizontalBlock"] {
    background: var(--nav-bg) !important;
    padding: 0.5rem 1rem !important;
    border-radius: 0 0 15px 15px;
}

[data-testid="stHorizontalBlock"] .st-c7 {
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

[data-testid="stHorizontalBlock"] .st-c7[aria-selected="true"] {
    background: var(--primary-red) !important;
    border-radius: 8px !important;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .news-image {
        height: 120px;
    }
    
    .main-title {
        font-size: 2rem !important;
    }
    
    .article-title {
        font-size: 1.2rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# --- SECRETS & API ---
try:
    API_KEY = st.secrets["newsapi_key"]
except KeyError:
    st.error("""
        **Configuration Required**  
        Create `.streamlit/secrets.toml` with:  
        ```
        newsapi_key = "YOUR_API_KEY"
        ```
    """)
    st.stop()

# --- CACHED DATA FETCHER ---
@st.cache_data(ttl=60*5, show_spinner=False)
def fetch_news_cached(topic: str, search_query=None):
    try:
        if search_query:
            url = f"https://newsapi.org/v2/everything?q={search_query}&apiKey={API_KEY}"
        else:
            url = f"{TOPICS[topic]['url']}&apiKey={API_KEY}"
        
        with st.spinner("📡 Fetching latest news..."):
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json().get("articles", [])
    
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request Error: {str(req_err)}")
        st.error(f"📡 Network error: {str(req_err).split('(')[0]}")
    except KeyError as key_err:
        logging.error(f"Key Error: {str(key_err)}")
        st.error(f"🔑 Missing data: {str(key_err)}")
    except Exception as e:
        logging.error(f"Unexpected Error: {str(e)}")
        st.error(f"⚠️ An unexpected error occurred")
    return []

# --- MODULAR COMPONENTS ---
def display_metadata(article, topic):
    st.markdown(
        f"<div class='metadata'>"
        f"<span class='category-tag'>{topic}</span>"
        f"<span class='timestamp'>{article.get('publishedAt', '')[:10]}</span>"
        f"</div>",
        unsafe_allow_html=True
    )

def display_image(article):
    img_url = article.get("urlToImage", "https://via.placeholder.com/800x450?text=No+Image")
    story_url = article.get("url", "#")
    return st.markdown(
        f"<a href='{story_url}' target='_blank' aria-label='Open story'>"
        f"<img class='news-image' src='{img_url}' loading='lazy' alt='{article.get('title', 'News story image')}'>"
        f"</a>",
        unsafe_allow_html=True
    )

def display_content(article):
    story_url = article.get("url", "#")
    st.markdown(
        f"<h3 class='article-title'>"
        f"<a href='{story_url}' target='_blank'>{article.get('title', 'Untitled')}</a>"
        f"</h3>",
        unsafe_allow_html=True
    )
    
    desc = article.get("description", "No description available")
    st.markdown(f"<p class='article-desc'>{desc}</p>", unsafe_allow_html=True)
    
    author = article.get("author", "Unknown Author")
    source = article.get("source", {}).get("name", "Unknown Source")
    st.markdown(
        f"<div class='article-meta'>"
        f"📝 {author} | 🏢 {source}"
        f"</div>",
        unsafe_allow_html=True
    )

# --- TOPICS CONFIG ---
TOPICS = {
    "Headlines": {
        "url": "https://newsapi.org/v2/top-headlines?country=us&pageSize=50",
        "icon": "newspaper"
    },
    "World": {
        "url": "https://newsapi.org/v2/top-headlines?category=general&pageSize=50",
        "icon": "globe"
    },
    "Business": {
        "url": "https://newsapi.org/v2/top-headlines?category=business&pageSize=50",
        "icon": "briefcase"
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
    "Politics": {
        "url": "https://newsapi.org/v2/everything?q=politics&pageSize=50",
        "icon": "bank"
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
        "container": {"padding": "0!important", "background": "var(--nav-bg)"},
        "icon": {"color": "#FF4B4B", "font-size": "16px"},
        "nav-link": {
            "font-size": "14px",
            "margin": "0 0.5rem",
            "padding": "0.75rem 1rem",
            "transition": "all 0.2s ease",
        },
        "nav-link-selected": {
            "background": "var(--primary-red)",
            "box-shadow": "0 2px 8px rgba(255,75,75,0.25)"
        },
    }
)

# --- HEADER ---
st.markdown("<h1 class='main-title'>PY NEWS</h1>", unsafe_allow_html=True)

# --- LOTTIE ANIMATION ---
def load_lottie(filepath: str):
    with open(filepath) as f:
        return json.load(f)

st_lottie(load_lottie("news2.json"), speed=0.5, height=300, key="header-anim")

# --- MAIN APP ---
with st.container():
    # Sidebar
    with st.sidebar:
        st.markdown("## 🔍 News Search")
        search_query = st.text_input(
            "Enter keywords:",
            placeholder="AI, Climate, Elections...",
            help="Search across all news categories"
        )
        
        st.markdown("## 🌐 Categories")
        for topic in TOPICS:
            st.button(
                f"{TOPICS[topic]['icon']} {topic}",
                use_container_width=True,
                key=f"cat_{topic}"
            )
    
    # Content
    st.markdown(f"<h2 class='category-title'>{selected_topic} News</h2>", unsafe_allow_html=True)
    
    articles = fetch_news_cached(selected_topic, search_query if search_query else None)
    
    if articles:
        for article in articles[:25]:
            with st.container():
