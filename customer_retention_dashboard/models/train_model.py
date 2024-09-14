# models/train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
from customer_retention_dashboard.utils.load_data import load_customer_churn_data
from customer_retention_dashboard.utils.clean_data import clean_customer_data

# Load and preprocess data
df = load_customer_churn_data()
df = clean_customer_data(df)

def train_churn_model(df):
    """
    Train a Random Forest model to predict customer churn.
    """
    # Ensure the 'contract' column exists
    if 'contract' not in df.columns:
        raise KeyError("The 'contract' column is missing from the dataset.")

    # Define features and target
    feature_cols = ['tenure_in_months', 'monthly_charge', 'total_revenue', 'number_of_dependents']

    # One-hot encode the 'contract' column
    df = pd.get_dummies(df, columns=['contract'], drop_first=True)

    # Check the available one-hot encoded columns
    contract_columns = [col for col in df.columns if 'contract' in col]
    if not contract_columns:
        raise KeyError("Expected one-hot encoded columns for 'contract' are missing.")

    # Add the one-hot encoded contract columns to the feature list
    feature_cols += contract_columns

    # Prepare training data (X) and target (y)
    X = df[feature_cols]
    y = df['customer_status'].apply(lambda x: 1 if x == 'Churned' else 0)

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Initialize and train RandomForest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")

    # Save the trained model to disk
    joblib.dump(model, 'churn_model.pkl')
    print("Model saved to 'models/churn_model.pkl'")

if __name__ == "__main__":
    # Train the model
    train_churn_model(df)
