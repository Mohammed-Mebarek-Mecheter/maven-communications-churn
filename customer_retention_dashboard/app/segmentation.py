# app/segmentation.py
import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
from utils.load_data import load_customer_churn_data, load_zipcode_population_data
from utils.transform_data import transform_data
from utils.clean_data import clean_customer_data, clean_zipcode_population_data
from components.filters import apply_segmentation_filters

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

    # Apply segmentation filters
    filtered_df = apply_segmentation_filters(df)

    # Risk Group Segmentation - Enhanced
    st.subheader("Risk Group Segmentation")
    risk_group_count = filtered_df.groupby('tenure_risk').size().reset_index(name='count')
    fig_risk_group = px.pie(risk_group_count, values='count', names='tenure_risk',
                            title="Customer Distribution by Risk Group", hole=0.3)
    st.plotly_chart(fig_risk_group, use_container_width=True)

    # Contract Type and Internet Type Breakdown
    st.subheader("Customer Segmentation by Contract and Internet Type")
    col1, col2 = st.columns(2)
    with col1:
        contract_count = filtered_df.groupby('contract').size().reset_index(name='count')
        fig_contract = px.pie(contract_count, values='count', names='contract', title="Customers by Contract Type")
        st.plotly_chart(fig_contract, use_container_width=True)

    with col2:
        internet_count = filtered_df.groupby('internet_type').size().reset_index(name='count')
        fig_internet = px.pie(internet_count, values='count', names='internet_type', title="Customers by Internet Type")
        st.plotly_chart(fig_internet, use_container_width=True)

    # Geographical Churn Heatmap - Enhanced Interactivity
    st.subheader("Geographical Churn Map")
    map_metric = st.selectbox("Choose metric to display on map", ['estimated_5_year_clv', 'monthly_charge', 'total_revenue'])

    # Filter out negative values for map display
    map_df = filtered_df[filtered_df[map_metric] > 0]

    layer = pdk.Layer(
        'ScatterplotLayer',
        map_df,
        get_position='[longitude, latitude]',
        get_radius=map_metric,
        get_color='[200, 30, 0, 160]',
        pickable=True
    )

    view_state = pdk.ViewState(
        latitude=map_df['latitude'].mean(),
        longitude=map_df['longitude'].mean(),
        zoom=5,
        pitch=50
    )

    r = pdk.Deck(layers=[layer], initial_view_state=view_state)
    st.pydeck_chart(r)

    # Customer Segments Table - Enhanced with Revenue and Risk Summary
    st.subheader("Customer Segments Overview")
    segment_summary = filtered_df.groupby(['contract', 'internet_type']).agg({
        'customerid': 'count',
        'monthly_charge': 'mean',
        'estimated_5_year_clv': 'mean',
        'tenure_in_months': 'mean',
        'total_revenue': 'sum'
    }).reset_index()
    segment_summary.columns = ['Contract', 'Internet Type', 'Customer Count', 'Avg Monthly Charge', 'Avg CLV', 'Avg Tenure', 'Total Revenue']
    st.dataframe(segment_summary.style.format({
        'Avg Monthly Charge': '${:.2f}',
        'Avg CLV': '${:.2f}',
        'Avg Tenure': '{:.1f}',
        'Total Revenue': '${:,.2f}'
    }))

if __name__ == "__main__":
    main()
