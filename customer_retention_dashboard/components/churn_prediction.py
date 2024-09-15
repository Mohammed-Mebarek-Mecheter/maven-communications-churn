# components/churn_prediction.py

import pandas as pd

def predict_churn(model, input_data, feature_columns):
    """
    Predict churn probability using the pre-trained model.
    Ensure the input data has the same features as the model was trained on.
    """
    # One-hot encode the input data to match the training format
    input_data_encoded = pd.get_dummies(input_data, columns=['contract', 'internet_service', 'online_security'])

    # Align the input data with the trained feature columns
    input_data_encoded = input_data_encoded.reindex(columns=feature_columns, fill_value=0)

    # Make prediction
    churn_probability = model.predict_proba(input_data_encoded)[:, 1][0]

    return churn_probability
