import sys
import os
from pathlib import Path
import streamlit as st

# ✅ DEFINE PATH FIRST
current_dir = Path(__file__).resolve().parent
root_path = current_dir.parent

# ✅ THEN DEBUG
st.write("ROOT:", os.listdir(root_path))
st.write("SRC:", os.listdir(root_path / "src"))

# ✅ ADD TO PATH
sys.path.insert(0, str(root_path))

import streamlit as st
from src.data_processor import load_and_merge_data
import importlib

visuals = importlib.import_module("src.visuals")

render_financial_overview = visuals.render_financial_overview
render_geographic_analysis = visuals.render_geographic_analysis
from src.model_loader import load_model

st.set_page_config(page_title="Health Equity Tracker", layout="wide")

st.title("🏥 Health Equity & Social Needs Tracker")

# Load data
data, report = load_and_merge_data()
model = load_model()

# Sidebar
st.sidebar.header("Filters")
selected_city = st.sidebar.selectbox("Select City", sorted(data['CITY'].dropna().unique()))

# Layout
col1, col2 = st.columns([2, 1])

with col1:
    render_financial_overview(report)
    st.divider()
    render_geographic_analysis(data, selected_city)

with col2:
    st.subheader("🔮 Predictive Cost Tool")

    age = st.number_input("Age", 0, 110, 40)
    income = st.number_input("Income", 0, 200000, 40000)
    coverage = st.number_input("Coverage", 0, 200000, 10000)

    if st.button("Predict"):
        if model:
            pred = model.predict([[age, income, coverage]])[0]
            st.metric("Predicted Cost", f"${pred:,.2f}")
        else:
            sim = (income * 0.02) + (age * 10) - (coverage * 0.01)
            st.metric("Simulated Cost", f"${max(sim,0):,.2f}")
