import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import json

# Set page configuration
st.set_page_config(
    page_title="Employment & Industry Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load animation (optional, make sure lottie file is in your project)
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Lottie animation (optional)
# animation = load_lottiefile("animations/industry.json")  # Add your own path
# st_lottie(animation, height=150)

# Load data
retained_industry_codes = pd.read_csv('dashboard_data/retained_industry_codes.csv', index_col=0)
retained_industry_codes.loc[retained_industry_codes.industry_code.str.len() > 50, 'industry_code'] = retained_industry_codes.industry_code.str.slice(0, 50) +'...'
dropped_industry_codes = pd.read_csv('dashboard_data/dropped_industry_codes.csv', index_col=0)
dropped_industry_codes.loc[dropped_industry_codes.industry_code.str.len() > 50, 'industry_code'] = dropped_industry_codes.industry_code.str.slice(0, 50) +'...'
industry_counts = pd.read_csv('dashboard_data/industry_counts.csv', index_col=0)
industry_counts = industry_counts.sort_values(by='count', ascending=False)
quarterly_employment = pd.read_csv('dashboard_data/quarterly_employment.csv', index_col=0)
employment_pct_change = pd.read_csv('dashboard_data/employment_pct_change.csv', index_col=0)
wage_change = pd.read_csv('dashboard_data/wage_change.csv', index_col=0)
wage_growth_data = pd.read_csv('dashboard_data/wage_growth_data.csv', index_col=0)

# Inject custom CSS
st.markdown("""
    <style>
        .main {
            background-color: #f5f7fa;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        h1, h2, h3 {
            color: #003366;
        }
        .css-18e3th9 {
            padding-top: 0px !important;
        }
        .st-emotion-cache-1v0mbdj {
            display: flex;
            justify-content: center;
            padding-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📊 Employment & Industry Dashboard")
st.markdown("#### Visual insights on employment outcomes and wage trends across industries and programs")

# --- Employment Status by Quarter ---
st.header("📅 Employment Status by Quarter")
st.markdown("""
> This bar chart shows the **distribution of employment status** across different quarters.  
There’s a visible decline in employment (~15%) over the 4-quarter span post-program exit.
""")
fig = px.bar(
    quarterly_employment,
    x="quarter",
    y="count",
    color="employment_status",
    barmode="stack",
    color_discrete_map={0: "#FF6B6B", 1: "#4ECDC4"},
    labels={"quarter": "Quarter", "count": "Count"},
    title=""
)
fig.update_layout(showlegend=False, height=400)
st.plotly_chart(fig, use_container_width=True)

# --- Employment Status Pie ---
st.header("🥧 Employment Status Distribution (Q4)")
pie_chart = quarterly_employment.groupby("employment_status")["count"].sum().reset_index()
pie_chart["employment_status"] = pie_chart["employment_status"].map({0: "Not Employed", 1: "Employed"})
col3, col4 = st.columns([1, 1])  # Equal width; adjust if needed (e.g., [1.5, 1])

with col3:
    fig = px.pie(
        pie_chart,
        names="employment_status",
        values="count",
        title="Employment Status at 4th Quarter After Program Exit",
        color_discrete_map={"Not Employed": "#FF6B6B", "Employed": "#1B998B"}
    )
    fig.update_traces(textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.markdown(
        """
        <div style="display: flex; flex-direction: column; justify-content: center; height: 100%;">
            <h3 style="text-align: left;">Key Insights</h3>
            <ul style="list-style-position: inside; padding-left: 0; text-align: left;">
                <li>Majority of individuals are <b>employed</b> by the fourth quarter.</li>
                <li>Roughly <b>15-20% remain unemployed</b> after program completion.</li>
                <li>Continued support post-program could potentially reduce unemployment.</li>
                <li>Pie chart shows a clear visual split between employment outcomes.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Wage Growth Analysis ---
st.header("📈 Wage Growth Analysis by Program")

col1, col2 = st.columns(2)
with col1:
    fig1 = px.bar(
        wage_growth_data.sort_values(by="wage_growth_percent", ascending=False),
        x="program",
        y="wage_growth_percent",
        title="Wage Growth Percentage",
        text="wage_growth_percent",
        color_discrete_sequence=["#118ab2"],
        labels={
            "program": "Program Name",
            "wage_growth_percent": "Wage Growth (%)"
        }
    )
    fig1.update_traces(texttemplate='%{text}%', textposition='outside')
    fig1.update_layout(yaxis=dict(range=[0, wage_growth_data["wage_growth_percent"].max() * 1.2]))
    fig1.update_layout(height=450)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(
        wage_growth_data.sort_values(by="dollar_wage_growth_for_each_day_spent_in_program", ascending=False),
        x="program",
        y="dollar_wage_growth_for_each_day_spent_in_program",
        title="Dollar Wage Growth per Day in Program",
        text="dollar_wage_growth_for_each_day_spent_in_program",
        color_discrete_sequence=["#ef476f"],
        labels={
            "program": "Program Name",
            "dollar_wage_growth_for_each_day_spent_in_program": "$ Wage Growth per Day"
        }
    )
    fig2.update_traces(texttemplate='$%{text}', textposition='outside')
    fig2.update_layout(yaxis=dict(range=[0, wage_growth_data["dollar_wage_growth_for_each_day_spent_in_program"].max() * 1.2]))
    fig2.update_layout(height=450)
    st.plotly_chart(fig2, use_container_width=True)

fig3 = px.scatter(
    wage_growth_data,
    x="days_in_program",
    y="wage_growth_percent",
    text="program",
    title="Days in Program vs. Wage Growth",
    labels={"days_in_program": "Days in Program", "wage_growth_percent": "Wage Growth (%)"},
    color_continuous_scale="Viridis", 
    size="participant_count",  # Set marker size based on participant_count
    size_max=20
)
fig3.update_traces(textposition='top center')
st.plotly_chart(fig3, use_container_width=True)

# --- Industries by Wage Change ---
st.header("🏭 Industries by Wage Change")

col1, col2 = st.columns(2)
wage_change.industry_code = wage_change.industry_code.astype(str).str.slice(0, 75)
df_top = wage_change.groupby("industry_code")["wage_change"].mean().nlargest(20).reset_index()
df_bottom = wage_change.groupby("industry_code")["wage_change"].mean().nsmallest(20).reset_index()

with col1:
    st.subheader("Top 20 Industries")
    fig = px.bar(df_top, 
        x="wage_change", 
        y="industry_code", 
        orientation="h", 
        text="wage_change", 
        color_discrete_sequence=["#06d6a0"],
        labels={
            "industry_code": "Industry Name",
            "wage_change": "Wage Growth (%)"
        })
    
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Bottom 20 Industries")
    fig = px.bar(df_bottom, 
                 x="wage_change", 
                 y="industry_code", 
                 orientation="h", 
                 text="wage_change", 
                 color_discrete_sequence=["#ff595e"],
                 labels={
                    "industry_code": "Industry Name",
                    "wage_change": "Wage Growth (%)"
                })
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# --- Industry Counts ---
st.header("🏷️ Top 20 Industry Code Counts")
fig = px.bar(
    industry_counts.head(20),
    x='industry_code',
    y='count',
    text='count',
    title='Industry Representation in Dataset',
    color_discrete_sequence=["#3a86ff"],
    labels={
        "industry_code": "Industry Name",
        "count": "Count of Employed"
    }
)
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# --- Retained vs Dropped Employment ---
st.header("🔄 Retention by Industry")

col1, col2 = st.columns(2)
with col1:
    st.subheader("20 Most Retained")
    fig = px.bar(
        retained_industry_codes.head(20),
        x="industry_code",
        y="count_of_retained_employment",
        text="count_of_retained_employment",
        title="Industries with Most Retained Employment",
        color_discrete_sequence=["#06d6a0"],
        labels={
            "industry_code": "Industry Name",
            "count_of_retained_employment": "Count of Employees"
        }
    )
    fig.update_layout(height=600, showlegend=False, xaxis=dict(tickangle=45))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("20 Least Retained")
    fig = px.bar(
        dropped_industry_codes.head(20),
        x="industry_code",
        y="count_of_dropped_employment",
        text="count_of_dropped_employment",
        title="Industries with Most Dropped Employment",
        color_discrete_sequence=["#ef476f"],
        labels={
            "industry_code": "Industry Name",
            "count_of_dropped_employment": "Count of Employees"
        }
    )
    fig.update_layout(height=600, showlegend=False, xaxis=dict(tickangle=45))
    st.plotly_chart(fig, use_container_width=True)

# --- Data Tables ---
st.header("📄 Data Preview")
with st.expander("📂 Click to Expand Data Tables"):
    st.write("**Quarterly Employment**")
    st.dataframe(quarterly_employment.head())

    st.write("**Wage Change by Industry**")
    st.dataframe(wage_change.head())

    st.write("**Employment % Change**")
    st.dataframe(employment_pct_change.head())

    st.write("**Wage Change by Program**")
    st.dataframe(wage_growth_data.head())
