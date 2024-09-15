# components/metric_cards.py

import streamlit as st

def display_kpis(overall_churn_rate, high_value_churn_rate, total_revenue_lost, customers_at_risk, active_customers, avg_clv):
    """
    Display KPI cards with added metrics and improved layout.
    """
    st.markdown("### Key Performance Indicators")

    # First set of KPIs
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            '<div class="metric-card"><div class="metric-value">' +
            f'{overall_churn_rate:.2f}%' +
            '</div><div class="metric-label">📉 Overall Churn Rate</div></div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="metric-card"><div class="metric-value">' +
            f'{active_customers:,}' +
            '</div><div class="metric-label">👥 Active Customers</div></div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<div class="metric-card"><div class="metric-value">' +
            f'{high_value_churn_rate:.2f}%' +
            '</div><div class="metric-label">⭐ High-Value Churn Rate</div></div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="metric-card"><div class="metric-value">' +
            f'${total_revenue_lost:,.2f}' +
            '</div><div class="metric-label">💸 Total Revenue Lost</div></div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            '<div class="metric-card"><div class="metric-value">' +
            f'{customers_at_risk:,}' +
            '</div><div class="metric-label">⚠️ Customers at Risk</div></div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="metric-card"><div class="metric-value">' +
            f'${avg_clv:,.2f}' +
            '</div><div class="metric-label">💰 Average CLV</div></div>',
            unsafe_allow_html=True
        )