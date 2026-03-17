import streamlit as st
import pandas as pd

def render_equity_charts(report_df):
    """
    Generates the Intersectional Cost Burden charts.
    """
    st.subheader("Healthcare Cost Burden (Vertical Equity Analysis)")
    st.bar_chart(data=report_df, x="RACE", y="TOTAL_CLAIM_COST")

def render_city_clusters(data_df, selected_city):
    """
    Generates the top 5 disease clusters for a specific city.
    """
    st.subheader(f"Top Disease Clusters in {selected_city}")
    city_stats = data_df[data_df['CITY'] == selected_city]['DESCRIPTION'].value_counts().head(5)
    st.bar_chart(city_stats)
