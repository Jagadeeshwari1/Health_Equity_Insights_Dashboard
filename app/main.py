import sys
import os
from pathlib import Path

# --- 1. DYNAMIC PATHING CONFIGURATION ---
# This identifies the folder 'health_equity_insights_dashboard'
# and adds it to the Python path so 'src' can be found.
current_dir = Path(__file__).resolve().parent
root_path = current_dir.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

# --- 2. IMPORTS ---
import streamlit as st
import pandas as pd
import joblib
from src.data_processor import load_and_merge_data
from src.visuals import render_financial_overview, render_geographic_analysis

# --- 3. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CareGap | Health Equity Tracker",
    page_icon="🏥",
    layout="wide"
)

# --- 4. DATA & MODEL LOADING ---
@st.cache_data
def get_cached_data():
    """Loads and merges data once to save memory on the cloud server."""
    return load_and_merge_data()

try:
    data, report = get_cached_data()
    
    # Attempt to load the trained model
    model_path = root_path / "models" / "cost_predictor.pkl"
    if model_path.exists():
        model = joblib.load(model_path)
    else:
        model = None

    # --- 5. APP HEADER ---
    st.title("🏥 Health Equity & Social Needs Tracker")
    st.markdown("""
    Analyzing the intersection of **Income**, **Location**, and **Healthcare Coverage** to identify gaps in **Vertical Equity** across California.
    """)

    # --- 6. SIDEBAR FILTERS ---
    st.sidebar.header("Geography & Economic Filters")
    
    # Filter by County
    all_counties = sorted(data['COUNTY'].unique())
    selected_county = st.sidebar.selectbox("Select County", all_counties, index=0)
    
    # Filter by Income Tier (Low, Middle, High)
    income_options = sorted(data['INCOME_TIER'].unique())
    selected_incomes = st.sidebar.multiselect(
        "Income Tiers", 
        income_options, 
        default=income_options
    )

    # --- 7. FILTERING LOGIC ---
    filtered_data = data[
        (data['COUNTY'] == selected_county) & 
        (data['INCOME_TIER'].isin(selected_incomes))
    ]
    
    # Filter report based on Income Tiers selected
    filtered_report = report[report['INCOME_TIER'].isin(selected_incomes)]

    # --- 8. DASHBOARD LAYOUT ---
    col1, col2 = st.columns([2, 1])

    with col1:
        # Visuals from src/visuals.py
        render_financial_overview(filtered_report)
        st.divider()
        render_geographic_analysis(filtered_report, selected_county)

    with col2:
        st.subheader("🔮 Predictive Risk Engine")
        st.info("Estimating individual financial burden based on SDOH factors.")
        
        age = st.number_input("Patient Age", 0, 110, 45)
        user_income = st.number_input("Annual Income ($)", 0, 500000, 45000)
        coverage = st.number_input("Current Healthcare Coverage ($)", 0, 500000, 15000)
        
        if st.button("Calculate Predicted Burden"):
            if model:
                # Use real Random Forest prediction
                # Note: Input must match the training features [AGE, INCOME, HEALTHCARE_COVERAGE]
                prediction = model.predict([[age, user_income, coverage]])[0]
                st.metric("Model Predicted Cost", f"${prediction:,.2f}")
            else:
                # Fallback Simulation Mode (prevents crash if .pkl is missing)
                simulated_cost = (user_income * 0.025) + (age * 12) - (coverage * 0.01)
                st.metric("Simulated Predicted Cost", f"${max(0, simulated_cost):,.2f}")
                st.warning("Running in simulation: Ensure cost_predictor.pkl is in /models")

    # --- 9. DATA PREVIEW ---
    with st.expander("🔍 View Raw Patient Data for this County"):
        st.dataframe(filtered_data[['Id', 'CITY', 'INCOME', 'HEALTHCARE_EXPENSES', 'HEALTHCARE_COVERAGE']].head(100))

except Exception as e:
    st.error("⚠️ Application Error")
    st.exception(e)
    st.info("Check that 'src', 'data', and 'models' folders exist in your GitHub repository.")
