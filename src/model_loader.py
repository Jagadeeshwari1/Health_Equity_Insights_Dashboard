import joblib
from pathlib import Path

def load_model():
    root = Path(__file__).parents[1]
    model_path = root / "models" / "cost_predictor.pkl"

    if model_path.exists():
        return joblib.load(model_path)
    return None
