import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_lottie import st_lottie
import json

# Set page configuration
st.set_page_config(
    page_title="Data for Hope Workforce Development Dashboard",
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
dropped_industry_codes = pd.read_csv('dashboard_data/dropped_industry_codes.csv', index_col=0)
industry_counts = pd.read_csv('dashboard_data/industry_counts.csv', index_col=0)
quarterly_employment = pd.read_csv('dashboard_data/quarterly_employment.csv', index_col=0)
df_wage_change = pd.read_csv('dashboard_data/wage_change_by_industry.csv', index_col=0)
df_wages_after = pd.read_csv('dashboard_data/wages_after_program_by_industry.csv', index_col=0)
wage_growth_data = pd.read_csv('dashboard_data/wage_growth_data.csv', index_col=0)
employment_pie = pd.read_csv('dashboard_data/employment_pie_chart.csv', index_col=0)
cat_meta_data = json.loads(open('dashboard_data/category_charts_meta.json').read())


st.markdown("""
    <style>
        /* Set background to light */
        .main {
            background-color: #f5f7fa !important;
        }
        
        /* Set text color to dark for better contrast */
        .css-18e3th9, h1, h2, h3, .stText {
            color: #003366 !important;
        }
        
        /* Change sidebar background color */
        .css-1d391kg {
            background-color: #ffffff !important;
        }
        
        /* Set input text color to dark */
        .stTextInput input, .stTextArea textarea {
            color: #333333 !important;
        }

        /* Ensure headers are light but readable */
        h1, h2, h3 {
            color: #003366;
        }

        .st-emotion-cache-1v0mbdj {
            display: flex;
            justify-content: center;
            padding-bottom: 20px;
        }

        .stSelectbox, .stMultiSelect {
            background-color: white !important;
            color: black !important;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📊 Data for Hope Workforce Development Dashboard")
st.markdown("#### Visual insights on employment outcomes and wage trends across industries and programs")

st.header("📚 Participant Characteristics")

cols = st.columns(2)  # create 2 columns

education_status = ["Type of Recognized Credential at Program Entry","School Status at Program Entry","Highest Education Level at Entry","Type of Work Experience at Program Entry"]

for i, key in enumerate(education_status):
    try:
        meta = cat_meta_data[key]
        df = pd.read_csv(meta["file"], index_col=0).reset_index()
        df = df.iloc[:, 1:]  # drop original index column
        df.columns = ['category', 'count']

        fig = px.bar(
            df.sort_values('count', ascending=True),
            x='count',
            y='category',
            orientation='h',
            title=meta["title"],
            labels={
                'category': meta["y"],
                'count': meta["x"]
            },
            color_discrete_sequence=[meta["color"]]
        )
        fig.update_layout(
            height=500,
            showlegend=False,
            margin=dict(l=50, r=30, t=50, b=30)
        )

        # Plot into the appropriate column
        with cols[i % 2]:
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.warning(f"⚠️ Could not load `{title}`: {e}")


# --- Employment Status by Quarter ---
st.header("📅 Employment Status by Quarter")
st.markdown("""
> This bar chart shows the **distribution of employment status** across different quarters.  
There’s a visible decline in employment (~15%) over the 4-quarter span post-program exit.
""")
quarterly_employment["employment_status"] = quarterly_employment["employment_status"].map({
    0: "Unemployed",
    1: "Employed"
})
# Plot with string labels now
fig = px.bar(
    quarterly_employment,
    x="quarter",
    y="count",
    color="employment_status",
    barmode="stack",
    color_discrete_map={"Unemployed": "#FF6B6B", "Employed": "#4ECDC4"},
    labels={"quarter": "Quarter", "count": "Count", "employment_status": "Employment Status"},
    title=""
)
fig.update_layout(showlegend=True, height=400)
st.plotly_chart(fig, use_container_width=True)

# --- Employment Status Pie ---
st.header("🥧 Employment Status Distribution after Program")
col3, col4 = st.columns([1, 1])  # Equal width; adjust if needed (e.g., [1.5, 1])

with col3:
    fig = px.pie(
        employment_pie,
        names="employment_status_after_program",
        values="count",
        title="Employment Status After Program Exit",
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
                <li>Majority of individuals are <b>unemployed</b> by the fourth quarter.</li>
                <li>Roughly <b>>35% become employed</b> after program completion.</li>
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

# --- Industries by Wage Change ---
st.header("🏭 Industries by Wage")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Top 20 Industries by Wage Change")
    fig = px.bar(df_wage_change, 
        x="wage_change", 
        y="industry_code", 
        orientation="h", 
        text="wage_change", 
        color_discrete_sequence=["#06d6a0"],
        labels={
            "industry_code": "Industry Name",
            "wage_change": "Wage After Program"
        })

    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top 20 Industries by Total Wages")
    fig = px.bar(df_wages_after, 
        x="total_wages_after", 
        y="industry_code", 
        orientation="h", 
        text="total_wages_after", 
        color_discrete_sequence=["#3a86ff"],
        labels={
            "industry_code": "Industry Name",
            "total_wages_after": "Total Wages After Program"
        })

    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


st.header("🏭 Training Program Characteristics")

side_by_side_keys = [
    "Occupational Skills Training Code",
    "Eligible Training Provider CIP Code"
]

col1, col2 = st.columns(2)

for i, key in enumerate(side_by_side_keys):
    try:
        meta = cat_meta_data[key]
        df = pd.read_csv(meta["file"], index_col=0).reset_index()
        df = df.iloc[:, 1:]  # drop original index column
        df.columns = ['category', 'count']

        fig = px.bar(
            df.sort_values('count', ascending=True),
            x='count',
            y='category',
            orientation='h',
            title=meta["title"],
            labels={
                'category': meta["y"],
                'count': meta["x"]
            },
            color_discrete_sequence=[meta["color"]]
        )
        fig.update_layout(
            height=500,
            showlegend=False,
            margin=dict(l=50, r=30, t=50, b=30)
        )

        with [col1, col2][i]:
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.warning(f"⚠️ Could not load `{key}`: {e}")



# --- Retained vs Dropped Employment ---
st.header("🔄 Retention by Industry")

col1, col2 = st.columns(2)

with col1:
    st.subheader("20 Most Retained")
    fig = px.bar(
        retained_industry_codes.sort_values(by="count_of_retained_employment", ascending=True),
        x="count_of_retained_employment",
        y="industry_code",
        text="count_of_retained_employment",
        orientation="h",
        title="Industries with Most Retained Employment",
        color_discrete_sequence=["#06d6a0"],
        labels={
            "industry_code": "Industry Name",
            "count_of_retained_employment": "Count of Employees"
        }
    )
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("20 Least Retained")
    fig = px.bar(
        dropped_industry_codes.sort_values(by="count_of_dropped_employment", ascending=True),
        x="count_of_dropped_employment",
        y="industry_code",
        text="count_of_dropped_employment",
        orientation="h",
        title="Industries with Most Dropped Employment",
        color_discrete_sequence=["#ef476f"],
        labels={
            "industry_code": "Industry Name",
            "count_of_dropped_employment": "Count of Employees"
        }
    )
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


# --- Data Tables ---
st.header("📄 Data Preview")
with st.expander("📂 Click to Expand Data Tables"):
    st.write("**Quarterly Employment**")
    st.dataframe(quarterly_employment.head())


    st.write("**Wage Change by Program**")
    st.dataframe(wage_growth_data.head())
