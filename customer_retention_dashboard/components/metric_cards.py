# components/metric_cards.py

import streamlit as st

def display_kpis(overall_churn_rate, high_value_churn_rate, total_revenue_lost, customers_at_risk):
    """
    Function to display the KPI cards in a row.
    """
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Overall Churn Rate", f"{overall_churn_rate:.2f}%")
    kpi2.metric("High-Value Churn Rate", f"{high_value_churn_rate:.2f}%")
    kpi3.metric("Total Revenue Lost to Churn", f"${total_revenue_lost:,.2f}")
    kpi4.metric("Customers at High Risk", f"{customers_at_risk:,}")
