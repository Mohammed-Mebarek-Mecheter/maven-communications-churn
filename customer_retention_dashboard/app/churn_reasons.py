# app/churn_reasons.py
import streamlit as st
import plotly.express as px
from customer_retention_dashboard.utils.load_data import load_customer_churn_data
from customer_retention_dashboard.utils.clean_data import clean_customer_data

st.title("Churn Reasons Analysis")

# Load and clean data
df = load_customer_churn_data()
df = clean_customer_data(df)

# Filter by churn category
churn_categories = df['churn_category'].dropna().unique().tolist()
selected_categories = st.multiselect("Select Churn Categories", churn_categories, default=churn_categories)

# Apply filter
filtered_df = df[df['churn_category'].isin(selected_categories)]

# Bar Chart: Customers Lost by Churn Reason
st.markdown("### Customers Lost by Churn Reason")
fig_churn_reason = px.bar(filtered_df.groupby('churn_reason').size().reset_index(name='count'),
                          x='churn_reason', y='count', title="Customers Lost by Churn Reason")
st.plotly_chart(fig_churn_reason, use_container_width=True)

# Revenue Loss by Churn Category
st.markdown("### Revenue Loss by Churn Category")
df_revenue_lost = filtered_df.groupby('churn_category').agg({'total_revenue': 'sum'}).reset_index()
fig_revenue_category = px.bar(df_revenue_lost, x='churn_category', y='total_revenue', title="Revenue Loss by Category")
st.plotly_chart(fig_revenue_category, use_container_width=True)
