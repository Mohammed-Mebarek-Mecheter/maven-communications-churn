# utils/transform_data.py
import pandas as pd

def calculate_churn_risk(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate churn risk levels based on tenure, contract, and refunds.
    """
    # Tenure-based risk
    df['tenure_risk'] = pd.cut(df['tenure_in_months'], bins=[-1, 12, 24, float('inf')],
                               labels=['High', 'Medium', 'Low'], right=False)

    # Contract-based risk
    df['contract_risk'] = df['contract'].apply(lambda x: 'High' if x == 'Month-to-month' else 'Low')

    # Refund-based risk
    df['refund_risk'] = df['total_refunds'].apply(lambda x: 'High' if x > 0 else 'Low')

    return df

def calculate_customer_lifetime_value(df: pd.DataFrame) -> pd.DataFrame:
    """
    Estimate the customer lifetime value (CLV) based on monthly charge and tenure.
    """
    df['estimated_5_year_clv'] = df['monthly_charge'] * 12 * 5  # Simple CLV estimate for 5 years
    return df

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply multiple transformations to the telecom customer churn data.
    """
    df = calculate_churn_risk(df)
    df = calculate_customer_lifetime_value(df)
    return df
