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

# Streamlit UI
st.markdown("""
    <style>
        .css-18e3th9 {
            padding-top: 0px !important;
        }
        .css-1d391kg {
            padding-top: 0px !important;
        }
        .st-emotion-cache-1v0mbdj {
            display: flex;
            justify-content: center;
            padding-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Employment & Industry Dashboard")

# Employment Status by Quarter
st.subheader("Employment Status by Quarter")
fig = px.bar(
    quarterly_employment, 
    x="quarter", 
    y="count", 
    color="employment_status", 
    barmode="stack", 
    labels={"quarter": "Quarter", "count": "Count"},
    title="Employment Status by Quarter"
)
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# Employment Status Pie Chart
st.subheader("Employment Status Distribution")
pie_chart = quarterly_employment.groupby("employment_status")["count"].sum().reset_index()
pie_chart["employment_status"] = pie_chart["employment_status"].map({0: "Not Employed", 1: "Employed"})
fig = px.pie(
    pie_chart, 
    names="employment_status", 
    values="count", 
    title="Employment Status at 4th Quarter After Program Exit",
    color_discrete_map={"Not Employed": "red", "Employed": "blue"}
)
st.plotly_chart(fig, use_container_width=False)

# Top & Bottom 20 Industries by Wage Change
st.subheader("Industries by Wage Change")
df_top = wage_change.groupby("industry_code")["wage_change"].mean().nlargest(20).reset_index()
df_bottom = wage_change.groupby("industry_code")["wage_change"].mean().nsmallest(20).reset_index()

st.write("### Top 20 Industries by Wage Change")
fig = px.bar(df_top, x="wage_change", y="industry_code", orientation="h", text="wage_change")
fig.update_layout(height=600, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.write("### Bottom 20 Industries by Wage Change")
fig = px.bar(df_bottom, x="wage_change", y="industry_code", orientation="h", text="wage_change")
fig.update_layout(height=600, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# Industry Counts
st.subheader("Industry Code Counts")
fig = px.bar(
    industry_counts.head(20),
    x='industry_code',
    y='count',
    text='count',
    title='Top 20 Industry Codes',
    labels={'industry_code': 'Industry Code', 'count': 'Count'}
)
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# Retained Employment by Industry
st.subheader("Retained Employment by Industry")
fig = px.bar(
    retained_industry_codes.head(30), 
    x="industry_code", 
    y="count_of_retained_employment", 
    text="count_of_retained_employment",
    title="Retained Employment by Industry"
)
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Least Retatined Employment by Industry")
fig = px.bar(
    dropped_industry_codes.head(30), 
    x="industry_code", 
    y="count_of_dropped_employment", 
    text="count_of_dropped_employment",
    title="Dropped Employment by Industry"
)
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# Data Tables
st.subheader("Data Tables")
st.write("### Quarterly Employment")
st.dataframe(quarterly_employment.head())

st.write("### Wage Change by Industry")
st.dataframe(wage_change.head())

st.write("### Employment Percentage Change")
st.dataframe(employment_pct_change.head())

