import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# 1. Load your merged data
# (Make sure patients.csv and encounters_part_1.csv are in your data folder)
data = pd.read_csv('data/patients.csv') # Simplified for example

# 2. Prepare Features (Age, Race, etc.)
# We convert categorical data to numbers so the model can read it
data['GENDER'] = data['GENDER'].map({'M': 0, 'F': 1})
X = data[['AGE', 'GENDER']] # Add more features like INCOME if available
y = data['TOTAL_CLAIM_COST'] # What we want to predict

# 3. Train the Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# 4. Save the Model to the pkl file
os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/cost_predictor.pkl')

print("Success: cost_predictor.pkl has been created in the /models folder!")
