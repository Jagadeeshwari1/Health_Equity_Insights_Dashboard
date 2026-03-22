import sys
import os
from pathlib import Path

# --- 1. DYNAMIC ROOT PATHING (CRITICAL FIX) ---
# This identifies '/mount/src/health_equity_insights_dashboard'
# and tells Python: "Look here for the 'src' folder"
current_dir = Path(__file__).resolve().parent
root_path = current_dir.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

# --- 2. IMPORTS ---
import streamlit as st
import pandas as pd
import joblib

# Now that the path is fixed, these imports will no longer error out
from src.data_processor import load_and_merge_data
from src.visuals import render_financial_overview, render_geographic_analysis

# --- 3. PAGE CONFIG ---
st.set_page_config(page_title="Health Equity Tracker", layout="wide", page_icon="🏥")

# --- 4. DATA LOADING ---
@st.cache_data
def get_data():
    return load_and_merge_data()

try:
    data, report = get_data()
    
    # Define Model Path using the root_path we found earlier
    model_path = root_path / "models" / "cost_predictor.pkl"
    model = joblib.load(model_path) if model_path.exists() else None

    # --- 5. UI HEADER ---
    st.title("🏥 Health Equity & Social Needs Tracker")
    st.markdown("Analyzing **Income**, **Location**, and **Healthcare Expenses** in California.")

    # --- 6. SIDEBAR FILTERS ---
    st.sidebar.header("Geography & Economic Filters")
    
    all_counties = sorted(data['COUNTY'].unique())
    selected_county = st.sidebar.selectbox("Select County", all_counties)
    
    income_options = sorted(data['INCOME_TIER'].unique())
    selected_incomes = st.sidebar.multiselect("Income Tiers", income_options, default=income_options)

    # --- 7. DASHBOARD CONTENT ---
    col1, col2 = st.columns([2, 1])

    with col1:
        # Filter report for visuals
        filtered_report = report[report['INCOME_TIER'].isin(selected_incomes)]
        render_financial_overview(filtered_report)
        st.divider()
        render_geographic_analysis(filtered_report, selected_county)

    with col2:
        st.subheader("🔮 Predictive Risk Engine")
        age = st.number_input("Age", 0, 110, 45)
        user_income = st.number_input("Annual Income ($)", 0, 500000, 45000)
        coverage = st.number_input("Coverage ($)", 0, 500000, 15000)
        
        if st.button("Calculate Predicted Burden"):
            if model:
                # Use real model prediction
                pred = model.predict([[age, user_income, coverage]])[0]
                st.metric("Predicted Annual Cost", f"${pred:,.2f}")
            else:
                # Fallback Simulation Mode
                sim_cost = (user_income * 0.02) + (age * 10) - (coverage * 0.01)
                st.metric("Simulated Cost", f"${max(0, sim_cost):,.2f}")
                st.warning("Model file not found. Running in simulation mode.")

except Exception as e:
    st.error("Application Error")
    st.exception(e)
