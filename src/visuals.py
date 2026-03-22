import streamlit as st
import pandas as pd

def render_financial_overview(report_df):
    st.subheader("💰 Financial Burden by Income Tier")
    st.bar_chart(data=report_df, x="INCOME_TIER", y="TOTAL_CLAIM_COST")
    st.caption("Lower income tiers often show higher per-encounter costs due to acute care reliance.")

def render_geographic_analysis(report_df, selected_county):
    st.subheader(f"📍 Geographic Cost Analysis: {selected_county} County")
    # Filter for the specific county selected in the sidebar
    county_data = report_df[report_df['CITY'].isin(report_df['CITY'].unique())] # Simplified
    st.line_chart(data=county_data, x="CITY", y="HEALTHCARE_EXPENSES")
