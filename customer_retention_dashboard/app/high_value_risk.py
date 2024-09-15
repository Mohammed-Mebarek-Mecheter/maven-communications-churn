# app/high_value_risk.py
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.load_data import load_customer_churn_data
from utils.transform_data import transform_data
from utils.clean_data import clean_customer_data

def main():

    # Load, clean, and transform data
    @st.cache_data(ttl=3600)
    def load_and_process_data():
        df = load_customer_churn_data()
        df = clean_customer_data(df)
        df = transform_data(df)
        return df

    df = load_and_process_data()

    # Filter for high-value customers (above median CLV)
    high_value_customers = df[df['estimated_5_year_clv'] > df['estimated_5_year_clv'].median()]

    # Allow user to filter by risk category (e.g., High, Medium, Low)
    risk_level = st.selectbox("Select Risk Level", ["All", "High", "Medium", "Low"])
    if risk_level != "All":
        high_value_customers = high_value_customers[high_value_customers['tenure_risk'] == risk_level]

    # Calculate key metrics
    num_high_value_at_risk = high_value_customers.shape[0]
    total_revenue_at_risk = high_value_customers['estimated_5_year_clv'].sum()
    avg_clv = high_value_customers['estimated_5_year_clv'].mean()
    avg_tenure = high_value_customers['tenure_in_months'].mean()

    # Display KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            '<div class="metric-card"><div class="metric-value">' +
            f'{num_high_value_at_risk}' +
            '</div><div class="metric-label">High-Value Customers at Risk</div></div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<div class="metric-card"><div class="metric-value">' +
            f'${total_revenue_at_risk:,.2f}' +
            '</div><div class="metric-label">Estimated Revenue at Risk</div></div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            '<div class="metric-card"><div class="metric-value">' +
            f'${avg_clv:,.2f}' +
            '</div><div class="metric-label">Average CLV (At Risk)</div></div>',
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            '<div class="metric-card"><div class="metric-value">' +
            f'{avg_tenure:.1f} months' +
            '</div><div class="metric-label">Average Tenure (At Risk)</div></div>',
            unsafe_allow_html=True
        )

    # CLV Distribution
    st.markdown("#### Customer Lifetime Value (CLV) Distribution")
    fig_clv = px.histogram(high_value_customers, x='estimated_5_year_clv', nbins=20, title="CLV Distribution", color_discrete_sequence=["#636EFA"])
    st.plotly_chart(fig_clv, use_container_width=True)

    # Revenue at Risk by Contract Type
    st.markdown("#### Revenue at Risk by Contract Type")
    revenue_by_contract = high_value_customers.groupby('contract').agg({
        'estimated_5_year_clv': 'sum',
        'customerid': 'count'
    }).reset_index()
    fig_revenue_contract = px.bar(revenue_by_contract, x='contract', y='estimated_5_year_clv', text='customerid',
                                  title="Revenue at Risk by Contract Type", labels={'estimated_5_year_clv': 'Revenue at Risk ($)', 'customerid': 'Customers'})
    st.plotly_chart(fig_revenue_contract, use_container_width=True)

    # Top 10 High-Value Customers at Risk
    st.markdown("#### Top 10 High-Value Customers at Risk")
    top_10_customers = high_value_customers.nlargest(10, 'estimated_5_year_clv')
    st.dataframe(top_10_customers[['customerid', 'tenure_in_months', 'monthly_charge', 'contract', 'estimated_5_year_clv']])

    # Option to explore individual customers
    st.markdown("### Explore Individual High-Value Customers")
    selected_customer = st.selectbox("Select Customer ID", high_value_customers['customerid'].unique())
    customer_details = high_value_customers[high_value_customers['customerid'] == selected_customer].iloc[0]

    st.write(f"**Customer ID**: {customer_details['customerid']}")
    st.write(f"**Tenure**: {customer_details['tenure_in_months']} months")
    st.write(f"**Monthly Charge**: ${customer_details['monthly_charge']:.2f}")
    st.write(f"**Contract**: {customer_details['contract']}")
    st.write(f"**Customer Lifetime Value (CLV)**: ${customer_details['estimated_5_year_clv']:,.2f}")
    st.write(f"**Tenure Risk**: {customer_details['tenure_risk']}")
    st.write(f"**Contract Risk**: {customer_details['contract_risk']}")
    st.write(f"**Refund Risk**: {customer_details['refund_risk']}")

if __name__ == "__main__":
    main()
