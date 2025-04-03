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
wage_growth_data = pd.read_csv('dashboard_data/wage_growth_data.csv', index_col=0)

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
st.markdown("""
- This bar chart shows the distribution of employment status across different quarters.
- Employment status is categorized as either 'Employed' or 'Not Employed'.
- There is a clear ~15% downward trend in employment status over the 4 quarters.
""")
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
st.markdown("""
- This pie chart visualizes the distribution of employment status (Employed vs Not Employed) in the 4th quarter after the program exit.
""")
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

st.subheader("Wage Growth Analysis by Program")
st.markdown("""
- These bar charts visualize the wage growths by program. As well as the number of days in the program.
""")
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


# Top & Bottom 20 Industries by Wage Change
st.subheader("Industries by Wage Change")
st.markdown("""
- The following two charts visualize industries by wage change, showing both the top 20 and bottom 20 industries.
- Wage change was calculated as the difference between the average wages before and after the program exit.
""")
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
st.markdown("""
- This bar chart displays the top 20 industries based on the number of occurrences in the dataset.
- This is an inclusive count that includes individuals who could have switched jobs.
""")
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
st.markdown("""
- This chart shows the industries with the highest number of retained employment after the program.
- It provides insights into which industries have retained the most workers over time.
""")
fig = px.bar(
    retained_industry_codes.head(30), 
    x="industry_code", 
    y="count_of_retained_employment", 
    text="count_of_retained_employment",
    title="Retained Employment by Industry"
)
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# Least Retained Employment by Industry
st.subheader("Least Retained Employment by Industry")
st.markdown("""
- This chart shows the industries with the highest number of employees that were employed and then were not employed.
""")
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
