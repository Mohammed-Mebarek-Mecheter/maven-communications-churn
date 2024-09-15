# app/churn_prediction.py
import streamlit as st
import pandas as pd
import joblib
from components.churn_prediction import predict_churn

def main():
    # Load pre-trained model and feature columns
    model = joblib.load('models/churn_model.pkl')
    feature_columns = joblib.load('models/churn_model_features.pkl')  # Load feature columns

    # Churn Prediction Form
    st.subheader("Predict Customer Churn")

    col1, col2 = st.columns(2)
    with col1:
        tenure = st.number_input("Tenure (months)", min_value=0, max_value=120, value=12)
        monthly_charge = st.number_input("Monthly Charge ($)", min_value=0.0, max_value=1000.0, value=50.0)
        total_charges = st.number_input("Total Charges ($)", min_value=0.0, max_value=10000.0, value=600.0)
    with col2:
        contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])

    if st.button("Predict Churn"):
        input_data = pd.DataFrame({
            'tenure_in_months': [tenure],
            'monthly_charge': [monthly_charge],
            'total_charges': [total_charges],
            'contract': [contract],
            'internet_service': [internet_service],
            'online_security': [online_security]
        })

        churn_probability = predict_churn(model, input_data, feature_columns)

        st.subheader("Churn Prediction Result")
        st.write(f"The probability of this customer churning is: {churn_probability:.2%}")

        if churn_probability > 0.5:
            st.warning("This customer is at high risk of churning!")
        else:
            st.success("This customer is likely to stay!")

if __name__ == "__main__":
    main()
