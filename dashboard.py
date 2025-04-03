import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(layout="wide")

# Load data
retained_industry_codes = pd.read_csv('dashboard_data/retained_industry_codes.csv', index_col=0)
dropped_industry_codes = pd.read_csv('dashboard_data/dropped_industry_codes.csv', index_col=0)
industry_counts = pd.read_csv('dashboard_data/industry_counts.csv', index_col=0)
industry_counts = industry_counts.sort_values(by='count', ascending=False)
quarterly_employment = pd.read_csv('dashboard_data/quarterly_employment.csv', index_col=0)
employment_pct_change = pd.read_csv('dashboard_data/employment_pct_change.csv', index_col=0)
wage_change = pd.read_csv('dashboard_data/wage_change.csv', index_col=0)

# Wage Growth Data
wage_growth_data = pd.read_csv('dashboard_data/wage_growth_data.csv', index_col=0)

# Streamlit UI
st.title("Employment & Industry Dashboard")

# Wage Growth Visualizations
st.subheader("Wage Growth Analysis by Program")

fig1 = px.bar(wage_growth_data, x="program", y="wage_growth_percent", title="Wage Growth Percentage", text="wage_growth_percent")
fig1.update_traces(texttemplate='%{text}%', textposition='outside')
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(wage_growth_data, x="program", y="dollar_wage_growth_for_each_day_spent_in_program", title="Dollar Wage Growth", text="dollar_wage_growth_for_each_day_spent_in_program")
fig2.update_traces(texttemplate='$%{text}', textposition='outside')
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.scatter(wage_growth_data, x="days_in_program", y="wage_growth_percent", text="program", title="Days in Program vs. Wage Growth",
                  labels={"days_in_program": "Days in Program", "wage_growth_percent": "Wage Growth Percentage"})
fig3.update_traces(textposition='top center')
st.plotly_chart(fig3, use_container_width=True)

# Existing Dashboard Components (Employment Status, Industry Analysis, etc.)
st.subheader("Employment Status by Quarter")
fig = px.bar(
    quarterly_employment, 
    x="quarter", 
    y="count", 
    color="employment_status", 
    barmode="stack", 
    title="Employment Status by Quarter"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Employment Status Distribution")
pie_chart = quarterly_employment.groupby("employment_status")["count"].sum().reset_index()
pie_chart["employment_status"] = pie_chart["employment_status"].map({0: "Not Employed", 1: "Employed"})
fig = px.pie(pie_chart, names="employment_status", values="count", title="Employment Status at 4th Quarter After Program Exit")
st.plotly_chart(fig, use_container_width=False)

st.subheader("Industries by Wage Change")
df_top = wage_change.groupby("industry_code")["wage_change"].mean().nlargest(20).reset_index()
df_bottom = wage_change.groupby("industry_code")["wage_change"].mean().nsmallest(20).reset_index()

st.write("### Top 20 Industries by Wage Change")
fig = px.bar(df_top, x="wage_change", y="industry_code", orientation="h", text="wage_change")
st.plotly_chart(fig, use_container_width=True)

st.write("### Bottom 20 Industries by Wage Change")
fig = px.bar(df_bottom, x="wage_change", y="industry_code", orientation="h", text="wage_change")
st.plotly_chart(fig, use_container_width=True)
