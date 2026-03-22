import sys
import os
from pathlib import Path

# --- 1. DYNAMIC PATH INJECTION (CRITICAL FIX) ---
# This finds 'health_equity_insights_dashboard' and adds it to the Python path.
# This ensures 'from src.xxx' works on Streamlit Cloud.
current_dir = Path(__file__).resolve().parent
root_path = current_dir.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

# --- 2. IMPORTS ---
import streamlit as st
import pandas as pd
import joblib

# Now that the path is fixed, these imports will work perfectly
from src.data_processor import load_and_merge_data
from src.visuals import render_financial_overview, render_geographic_analysis

# --- 3. PAGE CONFIG ---
st.set_page_config(
    page_title="Health Equity & Social Needs Tracker",
    page_icon="🏥",
    layout="wide"
)

# --- 4. DATA LOADING ---
@st.cache_data
def get_dashboard_data():
    """Loads and caches data to prevent re-reading CSVs on every click."""
    return load_and_merge_data()

try:
    data, report = get_dashboard_data()
    
    # Define Model Path using the root_path we found earlier
    model_path = root_path / "models" / "cost_predictor.pkl"
    if model_path.exists():
        model = joblib.load(model_path)
    else:
        model = None

    # --- 5. UI HEADER ---
    st.title("🏥 Health Equity & Social Needs Tracker")
    st.markdown("### Analyzing Vertical Equity: Income, Location, and Healthcare Burden")
    st.divider()

    # --- 6. SIDEBAR FILTERS ---
    st.sidebar.header("Geography & Economic Filters")
    
    all_counties = sorted(data['COUNTY'].unique())
    selected_county = st.sidebar.selectbox("Select County", all_counties)
    
    income_options = sorted(data['INCOME_TIER'].unique())
    selected_incomes = st.sidebar.multiselect("Income Tiers", income_options, default=income_options)

    # --- 7. FILTERING LOGIC ---
    # Filter report based on user selection
    filtered_report = report[report['INCOME_TIER'].isin(selected_incomes)]

    # --- 8. DASHBOARD COLUMNS ---
    col1, col2 = st.columns([2, 1])

    with col1:
        # Visuals from src/visuals.py
        render_financial_overview(filtered_report)
        st.divider()
        render_geographic_analysis(filtered_report, selected_county)

    with col2:
        st.subheader("🔮 Predictive Risk Engine")
        st.info("Estimating individual financial risk based on SDOH factors.")
        
        age = st.number_input("Patient Age", 0, 110, 45)
        user_income = st.number_input("Annual Income ($)", 0, 500000, 45000)
        coverage = st.number_input("Healthcare Coverage ($)", 0, 500000, 15000)
        
        if st.button("Calculate Predicted Burden"):
            if model:
                # Features must match training: [AGE, INCOME, HEALTHCARE_COVERAGE]
                pred = model.predict([[age, user_income, coverage]])[0]
                st.metric("Predicted Annual Cost", f"${pred:,.2f}")
            else:
                # Fallback Simulation if .pkl is missing
                sim_cost = (user_income * 0.025) + (age * 12) - (coverage * 0.01)
                st.metric("Simulated Predicted Cost", f"${max(0, sim_cost):,.2f}")
                st.warning("Model file not detected. Using heuristic calculation.")

    # --- 9. RAW DATA PREVIEW ---
    with st.expander("🔍 View Raw Patient Data (Sample)"):
        st.dataframe(data[['CITY', 'COUNTY', 'INCOME', 'HEALTHCARE_EXPENSES']].head(50))

except Exception as e:
    st.error("Application Error: Could not initialize dashboard.")
    st.exception(e)
    st.info("Check that 'src', 'data', and 'models' folders exist in your GitHub root.")
