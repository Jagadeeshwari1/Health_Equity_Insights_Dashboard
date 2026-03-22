import streamlit as st

def render_financial_overview(report_df):
    st.subheader("💰 Financial Burden Overview")
    st.bar_chart(report_df.set_index("CITY")[["HEALTHCARE_EXPENSES", "INCOME"]])

def render_geographic_analysis(data_df, selected_city):
    st.subheader(f"📍 Health Insights in {selected_city}")
    city_data = data_df[data_df['CITY'] == selected_city]

    if city_data.empty:
        st.warning("No data for selected city")
        return

    top_conditions = city_data['DESCRIPTION'].value_counts().head(5)
    st.bar_chart(top_conditions)
