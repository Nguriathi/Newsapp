PY NEWS
https://py-news.streamlit.app/

Overview
PY NEWS is a modern, responsive news aggregator web application built with Streamlit. It fetches the latest news articles from various categories using the NewsAPI and presents them in an elegant, user-friendly interface with rich visuals and smooth navigation.

The app features:

Topic-based news navigation with a sleek horizontal navbar.

Search functionality with a stylish integrated search icon.

Responsive design with mobile-friendly horizontal scrolling.

Eye-catching Lottie animations for enhanced user experience.

Article cards with images, metadata, and direct links to full stories.

Dark-themed UI with consistent styling and accessibility considerations.

Demo
https://py-news.streamlit.app/

Features
Multiple News Categories: Headlines, World, Business, Tech, Health, Science, Sports, Entertainment, Politics.

Search Bar: Quickly find news articles by keyword.

Responsive Navbar: Horizontal scrolling on mobile devices.

Lottie Animation: Engaging animation below the search bar.

Article Cards: Clickable images, titles, descriptions, and source info.

Dark Theme: Comfortable viewing with consistent color scheme.

Getting Started
Prerequisites
Python 3.7+

NewsAPI API Key (free to obtain at https://newsapi.org/)

Installation
Clone the repository:

bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo
Create and activate a virtual environment (optional but recommended):

bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
Install dependencies:

bash
pip install -r requirements.txt
Configure API Key:

Create a .streamlit/secrets.toml file in the root directory with the following content:


newsapi_key = "YOUR_NEWSAPI_KEY_HERE"
Replace "YOUR_NEWSAPI_KEY_HERE" with your actual NewsAPI key.

Running the App
Start the Streamlit app by running:

bash
streamlit run app.py
Replace app.py with your script filename if different.

Open your browser at the URL shown in the terminal (usually http://localhost:8501).

Project Structure

yourrepo/
│
├── app.py                # Main Streamlit app script
├── news2.json            # Lottie animation JSON file
├── requirements.txt      # Python dependencies
├── README.md             # This README file
├── .streamlit/
│   └── secrets.toml      # API key configuration (not committed)
└── assets/               # (Optional) images, logos, etc.
Dependencies
streamlit

requests

streamlit-lottie

streamlit-option-menu

Install them via:

bash
pip install streamlit requests streamlit-lottie streamlit-option-menu
Screenshots
![Navbar and Search](https://raw.githubusercontent.com/yourusername/yourrepo/main/navbar_searar with integrated search*

![Article Cards](https://raw.githubusercontent.com/yourusername/yourrepo/main/article_cards.pngcles displayed with images and metadata*

Contributing
Contributions are welcome! Please open issues or submit pull requests for bug fixes, improvements, or new features.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements
NewsAPI for providing the news data.

Streamlit for the amazing framework.

LottieFiles for the beautiful animations.



Thank you for checking out PY NEWS!
Stay informed with the latest news, beautifully presented.
