# utils/clean_data.py
import pandas as pd

def clean_customer_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the telecom customer churn data with additional validations and transformations.
    """
    # Drop rows without customer ID
    df.dropna(subset=['customerid'], inplace=True)

    # Fill missing values for categorical columns with 'Unknown'
    categorical_cols = ['gender', 'married', 'internet_type', 'contract', 'customer_status']
    df[categorical_cols] = df[categorical_cols].fillna('Unknown')

    # Fill missing values for numerical columns with 0
    numerical_cols = ['number_of_dependents', 'avg_monthly_long_distance_charges',
                      'avg_monthly_gb_download', 'monthly_charge', 'total_revenue', 'total_charges']
    df[numerical_cols] = df[numerical_cols].fillna(0)

    # Remove outliers and invalid data
    df = df[df['tenure_in_months'] >= 0]  # Remove invalid tenure
    df['monthly_charge'] = df['monthly_charge'].clip(lower=0)  # Monthly charge should not be negative

    # Convert columns to appropriate types
    df['tenure_in_months'] = df['tenure_in_months'].astype(int, errors='ignore')
    df['monthly_charge'] = df['monthly_charge'].astype(float, errors='ignore')

    # Standardize churn category text
    df['churn_category'] = df['churn_category'].str.title()

    return df

def clean_zipcode_population_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the zipcode population data.
    """
    df.dropna(subset=['zip_code'], inplace=True)
    df['population'] = df['population'].fillna(df['population'].median())
    df['zip_code'] = df['zip_code'].astype(str)

    return df
