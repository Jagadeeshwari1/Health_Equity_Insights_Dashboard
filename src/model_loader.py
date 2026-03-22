import joblib
import os

def load_prediction_model():
    """
    Loads the Random Forest pkl file using absolute pathing 
    to prevent Streamlit Cloud FileNotFoundError.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, 'models', 'cost_predictor.pkl')
    
    if not os.path.exists(model_path):
        return None
        
    return joblib.load(model_path)
