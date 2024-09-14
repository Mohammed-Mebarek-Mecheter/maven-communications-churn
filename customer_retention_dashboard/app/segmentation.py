# app/segmentation.py
import streamlit as st
import pandas as pd
import plotly.express as px
from customer_retention_dashboard.utils.load_data import load_customer_churn_data
from customer_retention_dashboard.utils.transform_data import transform_data
from customer_retention_dashboard.utils.clean_data import clean_customer_data

st.title("Customer Segmentation Analysis")

# Load and clean data
df = load_customer_churn_data()
df = clean_customer_data(df)
df = transform_data(df)

# Filters for segmentation
st.sidebar.markdown("## Filters")
tenure = st.sidebar.slider("Tenure (Months)", 0, df['tenure_in_months'].max(), (0, df['tenure_in_months'].max()))
contract = st.sidebar.multiselect("Contract Type", df['contract'].unique().tolist())
geography = st.sidebar.multiselect("City", df['city'].unique().tolist())

# Apply filters
filtered_df = df[(df['tenure_in_months'].between(*tenure)) & (df['contract'].isin(contract)) & (df['city'].isin(geography))]

# Risk Group Segmentation
st.markdown("### Risk Group Segmentation")
fig_risk_group = px.bar(filtered_df.groupby('tenure_risk').size(), title="Customers by Risk Group")
st.plotly_chart(fig_risk_group, use_container_width=True)

# Geographical Churn Heatmap
st.markdown("### Geographical Churn Heatmap")
fig_geo = px.density_mapbox(filtered_df, lat='latitude', lon='longitude', z='tenure_in_months', mapbox_style="open-street-map", title="Churn Risk by Geography")
st.plotly_chart(fig_geo, use_container_width=True)
