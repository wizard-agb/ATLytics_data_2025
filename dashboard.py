import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
@st.cache_data
def load_data():
    retained_industry_codes = pd.read_csv('dashboard_data/retained_industry_codes.csv', index_col=0)
    dropped_industry_codes = pd.read_csv('dashboard_data/dropped_industry_codes.csv', index_col=0)
    industry_counts = pd.read_csv('dashboard_data/industry_counts.csv', index_col=0)
    quarterly_employment = pd.read_csv('dashboard_data/quarterly_employment.csv', index_col=0)
    employment_pct_change = pd.read_csv('dashboard_data/employment_pct_change.csv', index_col=0)
    wage_change = pd.read_csv('dashboard_data/wage_change.csv', index_col=0)
    return retained_industry_codes, dropped_industry_codes, industry_counts, quarterly_employment, employment_pct_change, wage_change

# Load Data
retained_industry_codes, dropped_industry_codes, industry_counts, quarterly_employment, employment_pct_change, wage_change = load_data()

# Streamlit App Title
st.title("Employment Data Dashboard")

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Employment Status", "Wage Change Analysis", "Industry Trends", "Comments"])

# Define a uniform color scheme
custom_colors = px.colors.qualitative.Set1

if page == "Employment Status":
    st.header("Employment Status by Quarter")
    fig = px.bar(
        quarterly_employment, 
        x="quarter", 
        y="count", 
        color="employment_status", 
        barmode="stack", 
        title="Employment Status by Quarter",
        labels={"quarter": "Quarter", "count": "Count", "employment_status": "Employment Status"},
        color_discrete_sequence=custom_colors
    )
    st.plotly_chart(fig)
    
    st.header("Employment Status Distribution at 4th Quarter After Program Exit")
    pie_chart = quarterly_employment.groupby("employment_status")["count"].sum().reset_index()
    pie_chart["employment_status"] = pie_chart["employment_status"].map({0: "Not Employed", 1: "Employed"})
    fig = px.pie(
        pie_chart, 
        names="employment_status", 
        values="count", 
        color="employment_status", 
        color_discrete_map={"Not Employed": "red", "Employed": "blue"},
    )
    st.plotly_chart(fig)
    
    st.subheader("Quarterly Employment Data Table")
    st.dataframe(quarterly_employment)

elif page == "Wage Change Analysis":
    st.header("Top 20 Industries by Average Wage Change")
    top_wage_change = wage_change.groupby("industry_code")["wage_change"].mean().nlargest(20).reset_index()
    fig = px.bar(
        top_wage_change, 
        x="wage_change", 
        y="industry_code", 
        orientation="h", 
        color="industry_code",
        color_discrete_sequence=custom_colors,
    )
    st.plotly_chart(fig)
    
    st.header("Bottom 20 Industries by Average Wage Change")
    bottom_wage_change = wage_change.groupby("industry_code")["wage_change"].mean().nsmallest(20).reset_index()
    fig = px.bar(
        bottom_wage_change, 
        x="wage_change", 
        y="industry_code", 
        orientation="h", 
        color="industry_code",
        color_discrete_sequence=custom_colors,
    )
    st.plotly_chart(fig)
    
    st.subheader("Wage Change Data Table")
    st.dataframe(wage_change)

elif page == "Industry Trends":
    st.header("Industry Code Counts")
    fig = px.bar(
        industry_counts.nlargest(20, 'count'),
        x='industry_code',
        y='count',
        color='industry_code',
        color_discrete_sequence=custom_colors,
    )
    st.plotly_chart(fig)
    
    st.header("Retained Employment by Industry")
    fig = px.bar(
        retained_industry_codes.nlargest(30, 'count_of_retained_employment'),
        x="industry_code", 
        y="count_of_retained_employment", 
        color="industry_code",
        color_discrete_sequence=custom_colors,
    )
    st.plotly_chart(fig)
    
    st.subheader("Industry Counts Table")
    st.dataframe(industry_counts)

elif page == "Comments":
    st.header("Leave Your Comments Below")
    comment = st.text_area("Enter your comment:")
    if st.button("Submit"):
        st.success("Your comment has been recorded!")