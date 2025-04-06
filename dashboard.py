import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_lottie import st_lottie
import json

# Set page configuration
st.set_page_config(
    page_title="ATLytics x Data for Hope - Workforce Development Dashboard",
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
length_of_program_engagment = pd.read_csv('dashboard_data/length_of_program_engagement_bins.csv', index_col=0)
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
            color: black !important;
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

st.markdown(
    """
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin-bottom: 0;">Data for Hope Workforce Development Dashboard</h1>
            <p style="margin-top: 0;">A dashboard to give organizations that provide or support workforce development a better understanding of the value of their programs</p>
        </div>
        <div>
            <img src="https://atlytics.org/wp-content/uploads/2021/06/ATLytiCS-logo-2a.jpg" alt="Logo" style="height: 100px;">
        </div>
    </div>
    <hr style='margin:1em 0; border:1px solid #DDD;'>
    """,
    unsafe_allow_html=True
)

st.header("Participant Education Characteristics at Program Entry")
st.markdown("""
    <div style="border-left: 4px solid #D3D3D3; padding-left: 1em; margin: 1em 0; ">
        <h4 style="text-align: left; text-size: 16px; font-style: italic;">Key Insights</h4>
        <ul style="list-style-position: inside; padding-left: 0; text-align: left;">
            <li>This bar chart shows the <b>participant education statuses</b> at program entry.</li>  
            <li>The majority of program participants have <b>no formal credentials</b> and have at most a <b>high school diploma</b>.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)
cols = st.columns(2)  # create 2 columns

education_status = ["Type of Recognized Credential at Program Entry","School Status at Program Entry"]

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
        st.warning(f"⚠️ Could not load {meta["title"]}: {e}")

st.markdown("""<br><hr style='margin:2em 0; border:1px solid #DDD;'><br>""", unsafe_allow_html=True)
# --- Participant Characteristics at Program Entry ---
st.header("Participant Employment Characteristics at Program Entry")
st.markdown("""
    <div style="border-left: 4px solid #D3D3D3; padding-left: 1em; margin: 1em 0; ">
        <h4 style="text-align: left; text-size: 16px; font-style: italic;">Key Insights</h4>
        <ul style="list-style-position: inside; padding-left: 0; text-align: left;">
            <li>This bar chart shows the <b>participant employment statuses</b> at program entry.</li>  
            <li>The majority of program participants are <b>unemployed</b> and have <b>no prior work experience</b>.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)
work_characteristics = ["Work Status at Program Entry","Type of Work Experience at Program Entry"]

cols = st.columns(2)  

for i, key in enumerate(work_characteristics):
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
        st.warning(f"⚠️ Could not load {meta["title"]}: {e}")


# --- Employment Status by Quarter ---
st.markdown("""<br><hr style='margin:2em 0; border:1px solid #DDD;'><br>""", unsafe_allow_html=True)
st.header("Employment Status by Quarter")
st.markdown("""
    <div style="border-left: 4px solid #D3D3D3; padding-left: 1em; margin: 1em 0; ">
        <h4 style="text-align: left; text-size: 16px; font-style: italic;">Key Insights</h4>
        <ul style="list-style-position: inside; padding-left: 0; text-align: left;">
            <li>This bar chart shows the <b>distribution of unemployment status</b> across different quarters.</li>  
            <li>There’s a visible decline in unemployment (~19%) per quarter over the 4-quarter span post-program exit.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)
quarterly_employment["employment_status"] = quarterly_employment["employment_status"].map({
    0: "Unemployed",
    1: "Employed"
})
quarterly_employment = quarterly_employment.loc[quarterly_employment.employment_status == 'Unemployed']
# Plot with string labels now
fig = px.bar(
    quarterly_employment,
    x="quarter",
    y="count",
    barmode="stack",
    color_discrete_map={"Unemployed": "#FF6B6B"},
    labels={"quarter": "Quarter", "count": "Unemployment Count", "employment_status": "Employment Status"},
    title=""
)
fig.update_layout(showlegend=True, height=400)
st.plotly_chart(fig, use_container_width=True)

# --- Program Engagement Length Pie ---
st.markdown("""<br><hr style='margin:2em 0; border:1px solid #DDD;'><br>""", unsafe_allow_html=True)
st.header("Length of Program Engagement")
st.markdown("""
    <div style="border-left: 4px solid #D3D3D3; padding-left: 1em; margin: 1em 0; ">
        <h4 style="text-align: left; text-size: 16px; font-style: italic;">Key Insights</h4>
        <ul style="list-style-position: inside; padding-left: 0; text-align: left;">
            <li>The chart shows the <b>distribution of program engagement lengths</b> across different employment outcomes.  
            <li>There’s a visible increase in unemployment at 40-50 days of program engagement.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)
# Create grouped bar chart
fig = px.bar(
    length_of_program_engagment,
    x='length_of_program_engagement_bins',
    y='count',
    color='employment_status_label',
    barmode='group',
    labels={
        'length_of_program_engagement_bins': 'Length of Engagement (days)',
        'count': 'Number of People',
        'employment_status_label': 'Employment Status'
    },
    title='Employment Outcomes by Program Engagement Length'
)

fig.update_layout(margin=dict(l=50, r=30, t=50, b=30))

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)


# --- Employment Status Pie ---
st.markdown("""<br><hr style='margin:2em 0; border:1px solid #DDD;'><br>""", unsafe_allow_html=True)
st.header("Employment Status Distribution after Program")
col3, col4 = st.columns([1, 1])  # Equal width; adjust if needed (e.g., [1.5, 1])
employment_pie["employment_status_after_program"] = employment_pie["employment_status_after_program"].map({
    0: "Unemployed",
    1: "Employed"
})
with col3:
    fig = px.pie(
        employment_pie,
        names="employment_status_after_program",
        values="count",
        title="",
        color_discrete_map={"Not Employed": "#83c9ff", "Employed": "#0068c9"}
    )
    fig.update_traces(textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.markdown("""
        <div style=" padding-left: 1em; margin: 1em 0; ">
            <h4 style="text-align: left; text-size: 16px; font-style: italic;">Key Insights</h4>
            <ul style="list-style-position: inside; padding-left: 0; text-align: left;">
                <li>Majority of individuals are <b>unemployed</b> by the fourth quarter.</li>
                <li>Roughly <b>>40% become employed</b> after program completion.</li>
                <li>Continued support post-program could potentially reduce unemployment.</li>
                <li>Pie chart shows a clear visual split between employment outcomes.</li>
            </ul>
        </div>
    """, 
    unsafe_allow_html=True)



# --- Wage Growth Analysis ---
st.markdown("""<br><hr style='margin:2em 0; border:1px solid #DDD;'><br>""", unsafe_allow_html=True)
st.header("Wage Growth Analysis by Program")
st.markdown("""
        <div style="border-left: 4px solid #D3D3D3; padding-left: 1em; margin: 1em 0; ">
            <h4 style="text-align: left; text-size: 16px; font-style: italic;">Key Insights</h4>
            <ul style="list-style-position: inside; padding-left: 0; text-align: left;">
                <li>The chart shows wage growth of program participants that have provided wage data a quarter prior to program start and a quarter after program completion.</li>
                <li>Every program participant that provided wage data increased their wages <b>except for incumbent training program participants.</b> </li>
                <li>Although the Vocational Rehabilitation program seems to provide the best wage growth, there were only 2 samples, so the results could be skewed.</li>
                <li>A regression analysis was performed to see how each day spent in the program impacted a participants wage growth.</li>
                <li>Aside from Vocational Rehabilitation, participants in the Dislocated program could expect to see their wages increase by almost $6 for every day spent in the program.</li>
                <li>Adult education seemed to provide the least return on investment for the participants</li>
            </ul>
        </div>
    """, 
    unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    fig1 = px.bar(
        wage_growth_data.sort_values(by="wage_growth_percent", ascending=False),
        x="program",
        y="wage_growth_percent",
        title="Wage Growth Percentage",
        text="wage_growth_percent",
        color_discrete_sequence=["#0068c9"],
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
        color_discrete_sequence=["#83c9ff"],
        labels={
            "program": "Program Name",
            "dollar_wage_growth_for_each_day_spent_in_program": "$ Wage Growth per Day"
        }
    )
    fig2.update_traces(texttemplate='$%{text}', textposition='outside')
    fig2.update_layout(yaxis=dict(range=[0, wage_growth_data["dollar_wage_growth_for_each_day_spent_in_program"].max() * 1.2]))
    fig2.update_layout(height=450)
    st.plotly_chart(fig2, use_container_width=True)


st.markdown("""<br><hr style='margin:2em 0; border:1px solid #DDD;'><br>""", unsafe_allow_html=True)
st.header("Training Program Characteristics")
st.markdown("""
    <div style="border-left: 4px solid #D3D3D3; padding-left: 1em; margin: 1em 0; ">
        <h4 style="text-align: left; text-size: 16px; font-style: italic;">Key Insights</h4>
        <ul style="list-style-position: inside; padding-left: 0; text-align: left;">
            <li>These bar charts show the <b>skills training selected by participants</b> and the <b>training provider offered by the program</b>.</li>
            <li>Nursing and truck driving are the most popular skill sets trained</li>
            <li>Welding is also a notably popular skill set</li>
        </ul>
    </div>
""", unsafe_allow_html=True)
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


# --- Industry Counts ---
st.markdown("""<br><hr style='margin:2em 0; border:1px solid #DDD;'><br>""", unsafe_allow_html=True)
st.header("Top 20 Industry Code Counts")

st.markdown("""
    <div style="border-left: 4px solid #D3D3D3; padding-left: 1em; margin: 1em 0; ">
        <h4 style="text-align: left; text-size: 16px; font-style: italic;">Key Insights</h4>
        <ul style="list-style-position: inside; padding-left: 0; text-align: left;">
            <li>This bar chart shows the <b>count of industry employment</b>.</li>
            <li>This includes transitional workers who worked in multiple industries.</li>
            <li>Temporary help services is the most common industry</li>
            <li>Medical industries rank high in the 6th and 9th position</li>
            <li>Construction ranks high in the 10th position</li>
            <li>Restaurants rank highly as they usually have low skills requirements and are more easily accessible</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

fig = px.bar(
    industry_counts.head(20),
    x='industry_code',
    y='count',
    text='count',
    title='',
    color_discrete_sequence=["#0068c9"],
    labels={
        "industry_code": "Industry Name",
        "count": "Count of Employed"
    }
)
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# --- Industries by Wage Change ---
st.markdown("""<br><hr style='margin:2em 0; border:1px solid #DDD;'><br>""", unsafe_allow_html=True)
st.header("Industries by Wage")
st.markdown("""
    <div style="border-left: 4px solid #D3D3D3; padding-left: 1em; margin: 1em 0; ">
        <h4 style="text-align: left; text-size: 16px; font-style: italic;">Key Insights</h4>
        <ul style="list-style-position: inside; padding-left: 0; text-align: left;">
            <li>These bar charts show the <b>wage changes</b> before and after the program and the <b>total wages</b> after the program by industry.</li>
            <li>Most significant wage changes occur in manufacturing, administrative work, media, and graphic design industries.</li>
            <li>Manufacturing industries have the high total wages and wage changes, which may indicate the success of welding and apprenticeship programs.</li>
            <li>Motor vehicles and transportation industries have some of the highest total wages after the program indicating the success of Trucking programs.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.subheader("Top 20 Industries by Wage Change")
    fig = px.bar(df_wage_change, 
        x="wage_change", 
        y="industry_code", 
        orientation="h", 
        text="wage_change", 
        color_discrete_sequence=["#0068c9"],
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
        color_discrete_sequence=["#83c9ff"],
        labels={
            "industry_code": "Industry Name",
            "total_wages_after": "Total Wages After Program"
        })

    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


# --- Retained vs Dropped Employment ---
st.markdown("""<br><hr style='margin:2em 0; border:1px solid #DDD;'><br>""", unsafe_allow_html=True)
st.header("Retention by Industry")
st.markdown(
        """
        <div style="border-left: 4px solid #D3D3D3; padding-left: 1em; margin: 1em 0; ">
            <h4 style="text-align: left; text-size: 16px; font-style: italic;">Key Insights</h4>
            <ul style="list-style-position: inside; padding-left: 0; text-align: left;">
                <li>This bar chart shows the industries that <b>retained</b> and <b>dropped</b> the most employees.</li>
                <li><b>Temporary help services</b> is the most common industry with the most retained and dropped employment because workers should be in this industry temporarily.</li>
                <li><b>Medical industries</b> rank highly as the most retained employment.</li>
                <li><b>Restaurants</b> have the highest turnover which may reflect the highly accessible nature of the industry.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
col1, col2 = st.columns(2)

with col1:
    st.subheader("20 Industries with Most Retained Employment")
    fig = px.bar(
        retained_industry_codes.sort_values(by="count_of_retained_employment", ascending=True),
        x="count_of_retained_employment",
        y="industry_code",
        text="count_of_retained_employment",
        orientation="h",
        title="",
        color_discrete_sequence=["#0068c9"],
        labels={
            "industry_code": "Industry Name",
            "count_of_retained_employment": "Count of Employees"
        }
    )
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("20 Industries with Least Retained Employment")
    fig = px.bar(
        dropped_industry_codes.sort_values(by="count_of_dropped_employment", ascending=True),
        x="count_of_dropped_employment",
        y="industry_code",
        text="count_of_dropped_employment",
        orientation="h",
        title="",
        color_discrete_sequence=["#83c9ff"],
        labels={
            "industry_code": "Industry Name",
            "count_of_dropped_employment": "Count of Employees"
        }
    )
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


# --- Data Tables ---
st.header("📄 Further Investigations")
with st.expander("📂 Click to Expand Investigations"):
    st.write("**Areas for Improvement**")
    st.markdown(
        """
        <ul style="list-style-position: inside; padding-left: 0; text-align: left;">
            <li>Understand the level of engagement with each training program.</li>
            <li>Create pipelines to track each individual at each step of the program.</li>
            <li>Understand higher level economic impact of the training programs.</li>
            <li>Understand program sourcing metrics.</li>
        </ul>
        """,
        unsafe_allow_html=True
    )


