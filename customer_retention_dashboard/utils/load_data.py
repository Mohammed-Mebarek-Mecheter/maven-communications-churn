# utils/load_data.py
import os
import pandas as pd
import streamlit as st
from customer_retention_dashboard import config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@st.cache_resource(ttl=600)  # Cached for 10 minutes
def get_supabase_connection():
    from st_supabase_connection import SupabaseConnection
    # Set up the Supabase connection
    return st.connection(
        name="supabase",
        type=SupabaseConnection,
        ttl=None,
        url=config.SUPABASE_URL,
        key=config.SUPABASE_KEY,
    )

def load_data(table_name: str) -> pd.DataFrame:
    """
    Fetch data from Supabase and return as DataFrame.
    """
    supabase_client = get_supabase_connection()

    try:
        response = supabase_client.table(table_name).select("*").execute()
        df = pd.DataFrame(response.data)
        return df
    except Exception as e:
        st.error(f"Error fetching data from {table_name}: {str(e)}")
        return pd.DataFrame()  # Return empty DataFrame on error

# Load specific datasets
def load_customer_churn_data() -> pd.DataFrame:
    return load_data('telecom_customer_churn')

def load_zipcode_population_data() -> pd.DataFrame:
    return load_data('telecom_zipcode_population')
