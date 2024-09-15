# app/overview.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.load_data import load_customer_churn_data, load_zipcode_population_data
from utils.clean_data import clean_customer_data, clean_zipcode_population_data
from utils.transform_data import transform_data
from components.metric_cards import display_kpis

def main():

    # Load and preprocess data
    @st.cache_data(ttl=3600)
    def load_and_process_data():
        df_churn = load_customer_churn_data()
        df_population = load_zipcode_population_data()

        df_churn = clean_customer_data(df_churn)
        df_population = clean_zipcode_population_data(df_population)

        df = pd.merge(df_churn, df_population, on='zip_code', how='left')
        df = transform_data(df)
        return df

    df = load_and_process_data()

    # Calculate KPIs
    overall_churn_rate = (df['customer_status'] == 'Churned').mean() * 100
    high_value_churn_rate = df[df['estimated_5_year_clv'] > df['estimated_5_year_clv'].median()]['customer_status'].eq('Churned').mean() * 100
    total_revenue_lost = df[df['customer_status'] == 'Churned']['total_revenue'].sum()
    customers_at_risk = df[df['tenure_risk'] == 'High'].shape[0]
    active_customers = df[df['customer_status'] == 'Active'].shape[0]
    avg_clv = df['estimated_5_year_clv'].mean()

    # Display KPIs
    display_kpis(overall_churn_rate, high_value_churn_rate, total_revenue_lost, customers_at_risk, active_customers, avg_clv)

    # Churn Trends with Time Filter
    st.subheader("Churn Trends by Tenure")
    tenure_min, tenure_max = st.slider(
        "Select Tenure Range (Months)",
        int(df['tenure_in_months'].min()),
        int(df['tenure_in_months'].max()),
        (int(df['tenure_in_months'].min()), int(df['tenure_in_months'].max()))
    )

    # Filter data based on selected tenure range
    df_filtered = df[(df['tenure_in_months'] >= tenure_min) & (df['tenure_in_months'] <= tenure_max)]
    churn_trends = df_filtered.groupby('tenure_in_months')['customer_status'].apply(lambda x: (x == 'Churned').mean()).reset_index()
    churn_trends.columns = ['Tenure (Months)', 'Churn Rate']

    # Churn Trends Line Chart
    fig_trends = px.line(churn_trends, x='Tenure (Months)', y='Churn Rate', title="Churn Rate by Tenure")
    st.plotly_chart(fig_trends, use_container_width=True)

    # Churn by Customer Segments
    st.subheader("Churn by Customer Segment")
    segment_options = st.selectbox("Select Customer Segment", ["gender", "age", "contract", "internet_type"])
    fig_segment = px.bar(df_filtered[df_filtered['customer_status'] == 'Churned'].groupby(segment_options).size().reset_index(name='count'),
                         x=segment_options, y='count', title=f"Churn by {segment_options.capitalize()}")
    st.plotly_chart(fig_segment, use_container_width=True)

    # Optional: Add further interactive visualizations such as a geographic map or revenue breakdown.

if __name__ == "__main__":
    main()
