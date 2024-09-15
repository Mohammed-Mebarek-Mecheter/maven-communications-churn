# app.py
import streamlit as st
from streamlit_option_menu import option_menu
from app import overview, churn_reasons, high_value_risk, segmentation, churn_prediction, retention_strategies
from utils.load_data import load_customer_churn_data
from utils.clean_data import clean_customer_data
from streamlit_lottie import st_lottie
import json

# Page Configuration
st.set_page_config(page_title="Customer Retention Dashboard", page_icon="📊", layout="wide")

# Load custom CSS and favicon/logo
def load_custom_css():
    with open("assets/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_custom_css()

# Sidebar with metrics
st.sidebar.image("assets/company_logo.jpg", width=150)
df = clean_customer_data(load_customer_churn_data())
st.sidebar.metric("Total Customers", f"{len(df):,}")
st.sidebar.metric("Churned Customers", f"{len(df[df['customer_status'] == 'Churned']):,}")

#st.sidebar.markdown("---")
# Sidebar Menu
selected = option_menu(
    menu_title=None,
    options=["Overview", "Churn Analysis", "High-Value Customers", "Customer Segmentation", "Churn Prediction", "Retention Strategies"],
    icons=["house", "bar-chart", "star", "pie-chart", "graph-up", "people"],
    menu_icon="cast", orientation="horizontal",
    default_index=0,
)

# Render selected page
if selected == "Overview":
    overview.main()
elif selected == "Churn Analysis":
    churn_reasons.main()
elif selected == "High-Value Customers":
    high_value_risk.main()
elif selected == "Customer Segmentation":
    segmentation.main()
elif selected == "Churn Prediction":
    churn_prediction.main()
elif selected == "Retention Strategies":
    retention_strategies.main()

def load_lottie_file(filepath: str):
    """Function to load a Lottie animation from a JSON file."""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Lottie file not found: {filepath}")
        return None

def sidebar_lottie_animations():
    """Load and display Lottie animations for GitHub, LinkedIn, and Portfolio in the sidebar."""
    # Paths to Lottie JSON files
    lottie_github_path = "assets/images/github.json"
    lottie_linkedin_path = "assets/images/linkedin.json"
    lottie_portfolio_path = "assets/images/profile.json"

    # Load Lottie animations
    lottie_github = load_lottie_file(lottie_github_path)
    lottie_linkedin = load_lottie_file(lottie_linkedin_path)
    lottie_portfolio = load_lottie_file(lottie_portfolio_path)

    # Sidebar Lottie Animations with Links
    with st.sidebar.expander('### About Me'):
        st.markdown(
            """
            <div style='text-align: center;'>
                <h3>Made with ❤️ by Mebarek</h3>
                <p>Connect with me:</p>
            </div>
            """, unsafe_allow_html=True
        )

        # GitHub
        col1, col2 = st.columns([1, 3])
        with col1:
            st_lottie(lottie_github, height=30, width=30, key="lottie_github_sidebar")
        with col2:
            st.markdown("<a href='https://github.com/Mohammed-Mebarek-Mecheter/' target='_blank'>GitHub</a>", unsafe_allow_html=True)

        # LinkedIn
        col1, col2 = st.columns([1, 3])
        with col1:
            st_lottie(lottie_linkedin, height=30, width=30, key="lottie_linkedin_sidebar")
        with col2:
            st.markdown("<a href='https://www.linkedin.com/in/mohammed-mecheter/' target='_blank'>LinkedIn</a>", unsafe_allow_html=True)

        # Portfolio
        col1, col2 = st.columns([1, 3])
        with col1:
            st_lottie(lottie_portfolio, height=30, width=30, key="lottie_portfolio_sidebar")
        with col2:
            st.markdown("<a href='https://mebarek.pages.dev/' target='_blank'>Portfolio</a>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style='text-align: center;'>
                <p>Data source: <a href="https://mavenanalytics.io/challenges/maven-churn-challenge/8b3b32ff-fb5b-43ff-9fbf-c11f30ee14fe">Maven Analytics</a> | Last update: September 16, 2024</p>
            </div>
            """, unsafe_allow_html=True
        )

sidebar_lottie_animations()