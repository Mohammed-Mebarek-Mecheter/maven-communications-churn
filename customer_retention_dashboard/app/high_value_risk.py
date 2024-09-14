# app/high_value_risk.py
import streamlit as st
import plotly.express as px
from customer_retention_dashboard.utils.load_data import load_customer_churn_data
from customer_retention_dashboard.utils.transform_data import transform_data
from customer_retention_dashboard.utils.clean_data import clean_customer_data

st.title("High-Value Customers at Risk")

# Load, clean, and transform data
df = load_customer_churn_data()
df = clean_customer_data(df)
df = transform_data(df)

# Filter for high-value customers
high_value_customers = df[df['estimated_5_year_clv'] > df['estimated_5_year_clv'].median()]
high_risk_customers = high_value_customers[high_value_customers['tenure_risk'] == 'High']

# KPI: Number of High-Value Customers at Risk
num_high_value_at_risk = high_risk_customers.shape[0]
total_revenue_at_risk = high_risk_customers['estimated_5_year_clv'].sum()

st.metric("High-Value Customers at Risk", num_high_value_at_risk)
st.metric("Estimated Revenue at Risk", f"${total_revenue_at_risk:,.2f}")

# CLV Distribution
st.markdown("### Customer Lifetime Value (CLV) Distribution")
fig_clv = px.histogram(high_value_customers, x='estimated_5_year_clv', nbins=20, title="CLV Distribution")
st.plotly_chart(fig_clv, use_container_width=True)

# Top 10 High-Value Customers at Risk
st.markdown("### Top 10 High-Value Customers at Risk")
top_10_customers = high_risk_customers.nlargest(10, 'estimated_5_year_clv')
st.dataframe(top_10_customers[['customerid', 'tenure_in_months', 'monthly_charge', 'contract', 'estimated_5_year_clv']])
