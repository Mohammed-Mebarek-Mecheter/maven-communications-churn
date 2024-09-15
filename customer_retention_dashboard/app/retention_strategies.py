# app/retention_strategies.py
import streamlit as st
from utils.load_data import load_customer_churn_data
from utils.clean_data import clean_customer_data
from utils.transform_data import transform_data

def main():

    # Load and preprocess data
    @st.cache_data(ttl=3600)
    def load_and_process_data():
        df = load_customer_churn_data()
        df = clean_customer_data(df)
        df = transform_data(df)
        return df

    df = load_and_process_data()

    # Customer Selection
    st.subheader("Select a Customer for Retention Strategy")
    selected_customer = st.selectbox("Choose a customer ID", df['customerid'].unique())

    if selected_customer:
        customer_data = df[df['customerid'] == selected_customer].iloc[0]

        col1, col2 = st.columns(2)
        with col1:
            st.write("Customer Information")
            st.write(f"Tenure: {customer_data['tenure_in_months']} months")
            st.write(f"Monthly Charge: ${customer_data['monthly_charge']:.2f}")
            st.write(f"Contract: {customer_data['contract']}")
        with col2:
            st.write("Risk Factors")
            st.write(f"Tenure Risk: {customer_data['tenure_risk']}")
            st.write(f"Contract Risk: {customer_data['contract_risk']}")
            st.write(f"Refund Risk: {customer_data['refund_risk']}")

        # Add retention score and CLV
        retention_score = (0.4 if customer_data['tenure_risk'] == 'High' else 0.2) + \
                          (0.4 if customer_data['contract_risk'] == 'High' else 0.2) + \
                          (0.2 if customer_data['refund_risk'] == 'High' else 0.1)

        clv = customer_data['estimated_5_year_clv']

        # Display KPIs
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                '<div class="metric-card"><div class="metric-value">' +
                f'{retention_score:.2f}' +
                '</div><div class="metric-label">Retention Risk Score</div></div>',
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                '<div class="metric-card"><div class="metric-value">' +
                f'${clv:,.2f}' +
                '</div><div class="metric-label">Estimated Lifetime Value</div></div>',
                unsafe_allow_html=True
            )

        import plotly.express as px
        # Show risk factor bar chart
        risk_factors = ['Tenure Risk', 'Contract Risk', 'Refund Risk']
        risk_values = [0.4 if customer_data['tenure_risk'] == 'High' else 0.2,
                       0.4 if customer_data['contract_risk'] == 'High' else 0.2,
                       0.2 if customer_data['refund_risk'] == 'High' else 0.1]

        fig = px.bar(x=risk_factors, y=risk_values, title='Risk Factor Distribution',
                     labels={'x': 'Risk Factors', 'y': 'Values'}, color=risk_factors)
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
