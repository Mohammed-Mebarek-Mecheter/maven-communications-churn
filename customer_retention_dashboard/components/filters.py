# components/filters.py

import streamlit as st
import pandas as pd

def apply_segmentation_filters(df):
    """
    Applies sidebar filters for customer segmentation and returns filtered dataframe.
    Provides summary statistics based on filtered data.
    """
    st.sidebar.markdown("## Filters")

    # Tenure filter
    tenure_range = st.sidebar.slider(
        "Tenure (Months)",
        int(df['tenure_in_months'].min()),
        int(df['tenure_in_months'].max()),
        (int(df['tenure_in_months'].min()), int(df['tenure_in_months'].max()))
    )

    # Contract type filter
    contract_types = df['contract'].unique().tolist()
    selected_contracts = st.sidebar.multiselect("Contract Type", contract_types, default=contract_types)

    # Internet type filter
    internet_types = df['internet_type'].unique().tolist()
    selected_internet = st.sidebar.multiselect("Internet Type", internet_types, default=internet_types)

    # Monthly charge filter
    charge_range = st.sidebar.slider(
        "Monthly Charge ($)",
        min_value=0.0,
        max_value=float(df['monthly_charge'].max()),
        value=(0.0, float(df['monthly_charge'].max()))
    )

    # Customer status filter
    statuses = df['customer_status'].unique().tolist()
    selected_statuses = st.sidebar.multiselect("Customer Status", statuses, default=statuses)

    # Age group filter
    df['age_group'] = pd.cut(df['age'], bins=[0, 30, 45, 60, 100], labels=['18-30', '31-45', '46-60', '60+'])
    age_groups = df['age_group'].unique().tolist()
    selected_age_groups = st.sidebar.multiselect("Age Group", age_groups, default=age_groups)

    # Apply filters
    filtered_df = df[
        (df['tenure_in_months'].between(*tenure_range)) &
        (df['contract'].isin(selected_contracts)) &
        (df['internet_type'].isin(selected_internet)) &
        (df['monthly_charge'].between(*charge_range)) &
        (df['customer_status'].isin(selected_statuses)) &
        (df['age_group'].isin(selected_age_groups))
        ]

    # Display number of customers after filtering
    st.sidebar.markdown(f"**{len(filtered_df):,}** customers selected")

    # Show summary statistics
    avg_clv = filtered_df['estimated_5_year_clv'].mean()
    avg_tenure = filtered_df['tenure_in_months'].mean()
    st.sidebar.metric("Average CLV", f"${avg_clv:,.2f}")
    st.sidebar.metric("Average Tenure", f"{avg_tenure:.2f} months")

    # Add reset filters button
    if st.sidebar.button("Reset Filters"):
        st.experimental_rerun()

    return filtered_df


def apply_churn_analysis_filters(df):
    """
    Applies filters specific to churn analysis.
    """
    st.sidebar.markdown("## Churn Analysis Filters")

    # Churn category filter
    churn_categories = df['churn_category'].dropna().unique().tolist()
    selected_categories = st.sidebar.multiselect("Churn Categories", churn_categories, default=churn_categories)

    # Churn reason filter
    churn_reasons = df[df['churn_category'].isin(selected_categories)]['churn_reason'].dropna().unique().tolist()
    selected_reasons = st.sidebar.multiselect("Churn Reasons", churn_reasons, default=churn_reasons)

    # Apply filters
    filtered_df = df[
        (df['churn_category'].isin(selected_categories)) &
        (df['churn_reason'].isin(selected_reasons))
        ]

    # Display number of churned customers after filtering
    st.sidebar.markdown(f"**{len(filtered_df):,}** churned customers selected")

    return filtered_df

def apply_high_value_filters(df):
    """
    Applies filters specific to high-value customer analysis.
    """
    st.sidebar.markdown("## High-Value Customer Filters")

    # Ensure no negative values for the slider minimum
    min_clv = max(0, float(df['estimated_5_year_clv'].min()))

    # CLV threshold filter
    clv_threshold = st.sidebar.slider(
        "Customer Lifetime Value Threshold ($)",
        float(min_clv),  # Convert min_clv to float
        float(df['estimated_5_year_clv'].max()),
        value=float(df['estimated_5_year_clv'].median())
    )

    # Risk level filter
    risk_levels = ['Low', 'Medium', 'High']
    selected_risk_levels = st.sidebar.multiselect("Risk Levels", risk_levels, default=risk_levels)

    # Apply filters
    filtered_df = df[
        (df['estimated_5_year_clv'] >= clv_threshold) &
        (df['tenure_risk'].isin(selected_risk_levels))
        ]

    # Display number of high-value customers after filtering
    st.sidebar.markdown(f"**{len(filtered_df):,}** high-value customers selected")

    return filtered_df
