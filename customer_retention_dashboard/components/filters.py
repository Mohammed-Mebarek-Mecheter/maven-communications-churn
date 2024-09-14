# components/filters.py

import streamlit as st

def apply_segmentation_filters(df):
    """
    Applies sidebar filters for customer segmentation and returns filtered dataframe.
    """
    st.sidebar.markdown("## Filters")
    tenure = st.sidebar.slider("Tenure (Months)", 0, df['tenure_in_months'].max(), (0, df['tenure_in_months'].max()))
    contract = st.sidebar.multiselect("Contract Type", df['contract'].unique().tolist())
    geography = st.sidebar.multiselect("City", df['city'].unique().tolist())

    # Apply filters
    filtered_df = df[(df['tenure_in_months'].between(*tenure)) &
                     (df['contract'].isin(contract)) &
                     (df['city'].isin(geography))]

    return filtered_df
