import streamlit as st
import pandas as pd
import plotly.express as px
import os



def kpi_card(title, value, icon, border_color):

    st.markdown(
        f"""
        <div style="
            background-color:#FFFFFF;
            border-radius:12px;
            padding:18px;
            border-top:6px solid {border_color};
            box-shadow:0px 2px 8px rgba(0,0,0,0.15);
            text-align:center;
            height:120px;
        ">

        <div style="
            font-size:18px;
            color:#666666;
            font-weight:600;
        ">
            {icon} {title}
        </div>

        <div style="
            font-size:34px;
            font-weight:bold;
            color:#111111;
            margin-top:15px;
        ">
            {value}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Digital Detox Analytics",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

if os.path.exists("assets/banner.png"):

    st.image(

        "assets/banner.png",

        use_container_width=True

    )

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("""
<style>

div[data-testid="stMetric"]{
    background:white;
    border-radius:12px;
    padding:10px;
}

</style>
""",unsafe_allow_html=True)

# --------------------------------------------------
# Title
# --------------------------------------------------

st.markdown("""
# 📵 Digital Detox Analytics Dashboard

### AI-powered Multi-platform Social Media Analytics
""")

st.markdown(
"""
Multi-platform analytics for Digital Detox,
Mental Health and Social Media Discussions.
"""
)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

@st.cache_data
def load_data():

    return pd.read_csv(
        "data/processed/risk_dataset.csv"
    )

df = load_data()

TOPIC_NAMES = {
    1: "📚 Digital Detox & Productivity",
    2: "🌍 Multilingual Community Support",
    3: "📱 Screen Time & Phone Addiction",
    4: "🧠 Mental Health & Psychology",
    5: "🏥 Mental Health Services",
    6: "💚 Social Media & Dopamine"
}

df["topic_name"] = df["topic"].map(TOPIC_NAMES)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

if os.path.exists("assets/logo.png"):

    st.sidebar.image(

        "assets/logo.png",

        width=120

    )

st.sidebar.title("Digital Detox Analytics")
st.sidebar.markdown("---")

st.sidebar.header("Dashboard Filters")

platform = st.sidebar.multiselect(
    "Platform",
    options=sorted(df["platform"].unique()),
    default=sorted(df["platform"].unique())
)

sentiment = st.sidebar.multiselect(
    "Sentiment",
    options=sorted(df["sentiment"].unique()),
    default=sorted(df["sentiment"].unique())
)

topic = st.sidebar.multiselect(
    "Topic",
    options=sorted(df["topic_name"].unique()),
    default=sorted(df["topic_name"].unique())
)

st.sidebar.markdown("---")

st.sidebar.info("""
### 📵 Digital Detox Analytics

**Platforms**
- YouTube
- Telegram
- Bluesky
- Twitch

**AI Modules**
- Sentiment Analysis
- Topic Modeling
- Risk Detection
- AI Insights

**Developer**
Aishwarya Manyar
Abhishek Anand Jaiswal
Abhinav Kumar
Aditya Saurabh
""")

# --------------------------------------------------
# Apply Filters
# --------------------------------------------------

filtered = df[

    (df["platform"].isin(platform))

    &

    (df["sentiment"].isin(sentiment))

    &

    (df["topic_name"].isin(topic))

]

filtered = filtered.copy()

TOPIC_NAMES = {
    1: "📚 Digital Detox & Productivity",
    2: "🌍 Multilingual Community Support",
    3: "📱 Screen Time & Phone Addiction",
    4: "🧠 Mental Health & Psychology",
    5: "🏥 Mental Health Services",
    6: "💚 Social Media & Dopamine"
}

filtered["topic_name"] = filtered["topic"].map(TOPIC_NAMES)

if filtered.empty:
    st.warning("No data matches the selected filters. Please select different filter values.")
    st.stop()
    
# --------------------------------------------------
# Digital Wellness Index
# --------------------------------------------------

sentiment_score = {

    "Positive": 100,

    "Neutral": 60,

    "Negative": 20

}

filtered["sentiment_value"] = filtered["sentiment"].map(sentiment_score)

average_sentiment = filtered["sentiment_value"].mean()

risk_penalty = (

    len(

        filtered[

            filtered["risk_level"]=="High"

        ]

    )

    / len(filtered)

) * 100 if len(filtered) else 0

digital_wellness_index = round(

    average_sentiment - risk_penalty,

    1

)

digital_wellness_index = max(

    0,

    min(

        digital_wellness_index,

        100

    )

)

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------


total_posts = len(filtered)

positive_percent = (
    (filtered["sentiment"] == "Positive").mean() * 100
)

high_risk = (
    filtered["risk_level"] == "High"
).sum()

total_platforms = filtered["platform"].nunique()

dwi = digital_wellness_index

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    kpi_card(
        "Total Posts",
        total_posts,
        "📄",
        "#2563EB"
    )

with col2:
    kpi_card(
        "Positive %",
        f"{positive_percent:.1f}%",
        "😊",
        "#16A34A"
    )

with col3:
    kpi_card(
        "High Risk",
        high_risk,
        "⚠",
        "#DC2626"
    )

with col4:
    kpi_card(
        "Platforms",
        total_platforms,
        "🌍",
        "#7C3AED"
    )

with col5:
    kpi_card(
        "DWI",
        f"{dwi:.1f}/100",
        "⭐",
        "#F59E0B"
    )

st.divider()

if digital_wellness_index >= 80:

    st.success(
        "🟢 Excellent Digital Wellness"
    )

elif digital_wellness_index >= 60:

    st.info(
        "🟡 Moderate Digital Wellness"
    )

else:

    st.error(
        "🔴 Needs Digital Detox"
    )

# --------------------------------------------------
# Row 1
# Platform & Sentiment
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("📱 Platform Distribution")

    platform_chart = (

        filtered["platform"]

        .value_counts()

        .reset_index()

    )

    platform_chart.columns = ["Platform", "Posts"]

    fig = px.bar(

        platform_chart,

        x="Platform",

        y="Posts",

        text="Posts",

        color="Platform"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with col2:

    st.subheader("😊 Sentiment Distribution")

    sentiment_chart = (

        filtered["sentiment"]

        .value_counts()

        .reset_index()

    )

    sentiment_chart.columns = ["Sentiment", "Posts"]

    fig = px.pie(

        sentiment_chart,

        names="Sentiment",

        values="Posts",

        hole=0.45

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# --------------------------------------------------
# Row 2
# Topic & Risk
# --------------------------------------------------

col3, col4 = st.columns(2)

with col3:

    st.subheader("🧠 Topic Distribution")

    topic_chart = (

        filtered["topic_name"]

        .value_counts()

        .sort_index()

        .reset_index()

    )

    topic_chart.columns = ["Topic Name", "Posts"]

    fig = px.bar(

        topic_chart,

        x="Topic Name",

        y="Posts",

        text="Posts",

        color="Topic Name"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with col4:

    st.subheader("⚠ Risk Distribution")

    risk_chart = (

        filtered["risk_level"]

        .value_counts()

        .reset_index()

    )

    risk_chart.columns = ["Risk", "Posts"]

    fig = px.bar(

        risk_chart,

        x="Risk",

        y="Posts",

        text="Posts",

        color="Risk"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

st.divider()

# --------------------------------------------------
# Monthly Trend
# --------------------------------------------------

st.divider()

st.subheader("📈 Monthly Discussion Trend")

monthly = filtered.copy()

monthly["date"] = pd.to_datetime(
    monthly["date"],
    errors="coerce"
)

monthly["Month"] = monthly["date"].dt.to_period("M").astype(str)

monthly = (

    monthly.groupby("Month")

    .size()

    .reset_index(name="Posts")

)

fig = px.line(

    monthly,

    x="Month",

    y="Posts",

    markers=True,

    title="Digital Detox Discussions Over Time"

)

fig.update_layout(

    height=420,

    xaxis_title="Month",

    yaxis_title="Posts"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# --------------------------------------------------
# Word Cloud
# --------------------------------------------------

st.divider()

st.subheader("☁ Topic Word Cloud")

image_path = "outputs/topics/topic_wordcloud.png"

if os.path.exists(image_path):

    st.image(

        image_path,

        use_container_width=True

    )

else:

    st.warning("Word Cloud image not found.")
    
# --------------------------------------------------
# AI Insights
# --------------------------------------------------

st.divider()

st.subheader("🤖 AI Insights")

# --------------------------------------------------
# AI Generated Insights
# --------------------------------------------------

most_platform = filtered["platform"].mode()[0]

dominant_sentiment = filtered["sentiment"].mode()[0]

most_topic = (
    filtered["topic_name"].mode()[0]
    if "topic_name" in filtered.columns
    else f"Topic {filtered['topic'].mode()[0]}"
)

high_risk_posts = (
    filtered["risk_level"] == "High"
).sum()

positive_percent = (
    (filtered["sentiment"] == "Positive").mean() * 100
)

# ------------------------------------
# Dynamic Recommendation
# ------------------------------------

if digital_wellness_index >= 80:

    recommendation = (
        "Maintain current digital habits and continue promoting digital wellbeing."
    )

elif digital_wellness_index >= 60:

    recommendation = (
        "Encourage regular digital detox breaks and balanced screen usage."
    )

else:

    recommendation = (
        "Increase awareness campaigns and encourage users to reduce excessive screen time."
    )

# ------------------------------------
# Display Insights
# ------------------------------------

st.success(
    f"💚 Dominant Sentiment: **{dominant_sentiment}**"
)

st.info(
    f"📺 Most Active Platform: **{most_platform}**"
)

st.info(
    f"🧠 Most Discussed Topic: **{most_topic}**"
)

st.warning(
    f"⚠ High Risk Posts Detected: **{high_risk_posts}**"
)

st.success(
    f"⭐ Digital Wellness Index: **{digital_wellness_index:.1f}/100**"
)

st.info(
    f"📈 Positive Discussions: **{positive_percent:.1f}%**"
)

st.markdown("### 💡 AI Recommendation")

st.success(recommendation)
    
# --------------------------------------------------
# Platform Comparison
# --------------------------------------------------

st.divider()

st.subheader("📊 Platform Comparison")

comparison = filtered.groupby("platform").agg(
    Posts=("platform", "count"),
    Avg_Risk=("risk_score", "mean")
)

comparison["Positive %"] = (
    filtered[filtered["sentiment"] == "Positive"]
    .groupby("platform")
    .size()
    .div(comparison["Posts"])
    .mul(100)
)

comparison["Negative %"] = (
    filtered[filtered["sentiment"] == "Negative"]
    .groupby("platform")
    .size()
    .div(comparison["Posts"])
    .mul(100)
)

comparison["High Risk %"] = (
    filtered[filtered["risk_level"] == "High"]
    .groupby("platform")
    .size()
    .div(comparison["Posts"])
    .mul(100)
)

comparison = comparison.fillna(0)

comparison["Avg_Risk"] = comparison["Avg_Risk"].round(2)
comparison["Positive %"] = comparison["Positive %"].round(1)
comparison["Negative %"] = comparison["Negative %"].round(1)
comparison["High Risk %"] = comparison["High Risk %"].round(1)

st.dataframe(
    comparison,
    use_container_width=True
)

fig.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=50, b=20)
)

st.divider()

st.subheader("📥 Download AI Report")

with open(
    "outputs/insights/ai_insights_report.txt",
    "r",
    encoding="utf-8"
) as f:

    report = f.read()

st.download_button(
    label="📄 Download AI Insights Report",
    data=report,
    file_name="AI_Insights_Report.txt",
    mime="text/plain"
)

st.divider()

st.markdown(
"""
## 📌 Project Information

**Project:** Digital Detox Analytics

**Course:** Social Media Analytics Capstone

**Data Sources:**
- YouTube
- Telegram
- Bluesky
- Twitch

**Tech Stack:**
- Python
- Pandas
- SQLite
- Streamlit
- Plotly
- Scikit-learn
- NLTK
"""
)

st.divider()

st.markdown(
"""
---
### 📌 Digital Detox Analytics

Developed using:

- Python
- Streamlit
- SQLite
- Plotly
- NLTK
- Scikit-learn

© 2026 Capstone Project
"""
)

st.markdown("---")

st.caption(
"© 2026 Digital Detox Analytics | Developed by Group 1 | IIT Jodhpur Capstone Project"
)

