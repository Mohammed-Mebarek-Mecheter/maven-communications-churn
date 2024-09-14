# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import joblib
from utils.load_data import load_customer_churn_data
from utils.clean_data import clean_customer_data
from utils.transform_data import transform_data
from components.metric_cards import display_kpis
from components.filters import apply_segmentation_filters
import config

# Page Configuration
st.set_page_config(page_title="Customer Retention Dashboard", layout="wide")

# Custom CSS
def load_custom_css():
    with open("assets/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_custom_css()

# Sidebar Menu
with st.sidebar:
    selected = option_menu(
        "Maven Communications Dashboard",
        ["Overview", "Churn Reasons", "High-Value Customers", "Customer Segmentation"],
        icons=["house", "bar-chart", "star", "pie-chart"],
        menu_icon="cast",
        default_index=0,
    )

# Load and preprocess data
df = load_customer_churn_data()
df = clean_customer_data(df)
df = transform_data(df)

# Load pre-trained model
model = joblib.load('models/churn_model.pkl')

# Overview Page
if selected == "Overview":
    st.title("Maven Communications: Customer Retention Overview")

    # KPIs
    overall_churn_rate = (df['customer_status'] == 'Churned').mean() * 100
    high_value_churn_rate = df[df['estimated_5_year_clv'] > df['estimated_5_year_clv'].median()]['customer_status'].eq('Churned').mean() * 100
    total_revenue_lost = df[df['customer_status'] == 'Churned']['total_revenue'].sum()
    customers_at_risk = df[df['tenure_risk'] == 'High'].shape[0]

    # Display KPIs
    display_kpis(overall_churn_rate, high_value_churn_rate, total_revenue_lost, customers_at_risk)

    # Churn by Customer Segment
    st.markdown("## Churn by Customer Segment")
    segment_options = st.selectbox("Select Customer Segment", ["gender", "age", "contract"])
    fig_segment = px.bar(df[df['customer_status'] == 'Churned'].groupby(segment_options).size().reset_index(name='count'),
                         x=segment_options, y='count', title=f"Churn by {segment_options.capitalize()}")
    st.plotly_chart(fig_segment, use_container_width=True)

# Churn Reasons Page
elif selected == "Churn Reasons":
    st.title("Churn Reasons Analysis")

    # Filter by churn category
    churn_categories = df['churn_category'].dropna().unique().tolist()
    selected_categories = st.multiselect("Select Churn Categories", churn_categories, default=churn_categories)

    # Apply filter
    filtered_df = df[df['churn_category'].isin(selected_categories)]

    # Treemap for Churn Reasons
    st.markdown("### Revenue Lost by Churn Reason")
    fig_churn_reason = px.treemap(filtered_df, path=['churn_category', 'churn_reason'],
                                  values='total_revenue', title="Revenue Lost by Churn Reason")
    st.plotly_chart(fig_churn_reason, use_container_width=True)

# High-Value Customers Page
elif selected == "High-Value Customers":
    st.title("High-Value Customers at Risk")

    # Filter for high-value customers
    high_value_customers = df[df['estimated_5_year_clv'] > df['estimated_5_year_clv'].median()]
    high_risk_customers = high_value_customers[high_value_customers['tenure_risk'] == 'High']

    # KPI: High-Value Customers at Risk
    num_high_value_at_risk = high_risk_customers.shape[0]
    total_revenue_at_risk = high_risk_customers['estimated_5_year_clv'].sum()

    st.metric("High-Value Customers at Risk", num_high_value_at_risk)
    st.metric("Estimated Revenue at Risk", f"${total_revenue_at_risk:,.2f}")

    # Customer Cluster Scatter Plot
    st.markdown("### High-Value Customer Clusters")
    fig_scatter = px.scatter(high_value_customers, x='tenure_in_months', y='estimated_5_year_clv',
                             size='monthly_charge', color='contract', title="High-Value Customer Clusters")
    st.plotly_chart(fig_scatter, use_container_width=True)

# Customer Segmentation Page
elif selected == "Customer Segmentation":
    st.title("Customer Segmentation Analysis")

    # Apply segmentation filters from filters.py
    filtered_df = apply_segmentation_filters(df)

    # Risk Group Segmentation
    st.markdown("### Risk Group Segmentation")
    fig_risk_group = px.bar(filtered_df.groupby('tenure_risk').size().reset_index(name='count'),
                            x='tenure_risk', y='count', title="Customers by Risk Group")
    st.plotly_chart(fig_risk_group, use_container_width=True)

    # Geographical Churn Heatmap
    st.markdown("### Geographical Churn Heatmap")
    fig_geo = px.scatter_mapbox(filtered_df, lat='latitude', lon='longitude',
                                size='estimated_5_year_clv', color='tenure_risk',
                                mapbox_style="open-street-map", title="Customer Segmentation by Geography")
    st.plotly_chart(fig_geo, use_container_width=True)
