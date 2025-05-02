
# PY NEWS

Welcome to **PY NEWS**, a sleek and modern news aggregator web app built with [Streamlit](https://streamlit.io/) that brings you the latest headlines and stories from around the world - all in one place!

[🌐 Live Demo](https://py-news.streamlit.app/)

---

## Overview

PY NEWS fetches real-time news articles from various categories using the powerful [NewsAPI](https://newsapi.org/). It features a clean, dark-themed interface with:

- A horizontal, icon-enhanced navbar for easy topic navigation.
- An integrated search bar with a matching styled search icon.
- Responsive design optimized for desktop and mobile devices.
- Engaging Lottie animations to enhance user experience.
- Article cards with images, descriptions, and direct links to full stories.

---

## Features

- **Multiple Categories:** Headlines, World, Business, Tech, Health, Science, Sports, Entertainment, Politics.
- **Search Functionality:** Quickly find news by keywords.
- **Responsive Navbar:** Scrollable on smaller screens with icons for each category.
- **Lottie Animation:** Eye-catching animation below the search bar.
- **Clean Dark Theme:** Easy on the eyes with consistent styling.
- **Article Cards:** Includes images, metadata, author, source, and a “Continue to story” button.

---

## Getting Started

### Prerequisites

- Python 3.7 or higher
- A free API key from [NewsAPI](https://newsapi.org/)

### Installation

1. Clone the repository:

git clone https://github.com/yourusername/py-news.git
cd py-news


2. (Optional) Create and activate a virtual environment:

python -m venv venv

Windows
venv\Scripts\activate

macOS/Linux
source venv/bin/activate


3. Install dependencies:

pip install -r requirements.txt


4. Add your NewsAPI key:

Create a `.streamlit/secrets.toml` file in the project root with:

newsapi_key = "YOUR_NEWSAPI_KEY"


Replace `"YOUR_NEWSAPI_KEY"` with your actual key.

---

## Usage

Run the app locally with:

streamlit run app.py


Open the URL shown in your terminal (usually `http://localhost:8501`).

---

## Project Structure

py-news/
├── app.py # Main Streamlit app
├── news2.json # Lottie animation JSON file
├── requirements.txt # Python dependencies
├── README.md # This file
└── .streamlit/
└── secrets.toml # API key (not committed)


---

## Dependencies

- streamlit
- requests
- streamlit-lottie
- streamlit-option-menu

Install all via:

pip install streamlit requests streamlit-lottie streamlit-option-menu


---

## Screenshots

*Add screenshots or GIFs here showcasing the app’s UI and responsiveness.*

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the app.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- [NewsAPI](https://newsapi.org/) for the news data.
- [Streamlit](https://streamlit.io/) for the amazing framework.
- [LottieFiles](https://lottiefiles.com/) for beautiful animations.

---


---

Thank you for checking out PY NEWS! Stay informed, stay ahead.
