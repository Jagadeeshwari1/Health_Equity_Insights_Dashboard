from sklearn.ensemble import RandomForestRegressor
import joblib
import pandas as pd
import os

def train_and_save_model(df):
    # Defining features based on your new list: Income, Healthcare Expenses, etc.
    features = ['AGE', 'INCOME', 'HEALTHCARE_COVERAGE']
    target = 'TOTAL_CLAIM_COST'

    X = df[features].fillna(0)
    y = df[target].fillna(0)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/cost_predictor.pkl')
    print("Model updated for Income/Place features.")

# Usage:
# data, _ = load_and_merge_data()
# train_and_save_model(data)


