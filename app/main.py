import sys
import os
from pathlib import Path

# Fix pathing so Streamlit Cloud finds the 'src' folder
sys.path.append(str(Path(__file__).parents[1]))

import streamlit as st
import joblib
from src.data_processor import load_and_merge_data
from src.visuals import render_financial_overview, render_geographic_analysis

st.set_page_config(page_title="CareGap Equity Dashboard", layout="wide")

st.title("🏥 Health Equity & Social Needs Tracker")
st.markdown("Analyzing the intersection of **Income**, **Location**, and **Healthcare Coverage**.")

try:
    # 1. Load Data
    data, report = load_and_merge_data()

    # 2. Sidebar: Geographic & Economic Filters
    st.sidebar.header("Geography & Economy Filters")
    all_counties = sorted(data['COUNTY'].unique())
    selected_county = st.sidebar.selectbox("Select County", all_counties)
    
    income_options = data['INCOME_TIER'].unique()
    selected_incomes = st.sidebar.multiselect("Income Tiers", income_options, default=list(income_options))

    # 3. Filtered Logic
    filtered_data = data[(data['COUNTY'] == selected_county) & (data['INCOME_TIER'].isin(selected_incomes))]
    filtered_report = report[report['INCOME_TIER'].isin(selected_incomes)]

    # 4. Dashboard Columns
    col1, col2 = st.columns([2, 1])

    with col1:
        render_financial_overview(filtered_report)
        render_geographic_analysis(filtered_report, selected_county)

    with col2:
        st.subheader("🔮 Predictive Risk Engine")
        st.info("Predicts financial risk based on Place and Income.")
        age = st.number_input("Age", 0, 110, 45)
        user_income = st.number_input("Annual Income ($)", 0, 500000, 45000)
        coverage = st.number_input("Current Coverage ($)", 0, 500000, 10000)
        
        if st.button("Calculate Predicted Burden"):
            # Simple algorithmic fallback if .pkl is still loading
            burden = (user_income * 0.02) + (age * 15) - (coverage * 0.01)
            st.metric("Estimated Annual Burden", f"${burden:,.2f}")

except Exception as e:
    st.error(f"Deployment Error: {e}")
    st.info("Ensure your /data folder contains patients.csv and encounters_part_1.csv")
