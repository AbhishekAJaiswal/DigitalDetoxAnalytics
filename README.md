# 📵 Digital Detox Analytics

## AI-Powered Multi-Platform Social Media Analytics for Digital Wellbeing

Digital Detox Analytics is a Social Media Analytics Capstone Project that collects, processes, analyzes, and visualizes public discussions related to **Digital Detox**, **Screen Time**, **Social Media Addiction**, and **Mental Health** across multiple social media platforms.

The project integrates data engineering, natural language processing, machine learning, and interactive visualization to generate actionable insights regarding digital wellbeing.

---

# Project Objectives

The project aims to:

- Collect social media data from multiple platforms.
- Clean and preprocess noisy textual data.
- Analyze user sentiment.
- Discover hidden discussion topics using Topic Modeling.
- Detect potentially risky discussions.
- Compute a custom **Digital Wellness Index (DWI)**.
- Generate AI-driven insights.
- Visualize findings through an interactive Streamlit dashboard.

---

# Data Sources

The project collects publicly available discussions from:

- 📺 YouTube
- 💬 Telegram
- 🦋 Bluesky
- 🎮 Twitch

---

# Project Architecture

```
Social Media Platforms
        │
        ▼
YouTube   Telegram   Bluesky   Twitch
        │
        ▼
      Data Collection
        │
        ▼
     Merge Dataset
        │
        ▼
    SQLite Database
        │
        ▼
 Data Cleaning & Preprocessing
        │
        ▼
    Topic Filtering
        │
        ▼
 Feature Engineering
        │
        ▼
 Sentiment Analysis (VADER)
        │
        ▼
 Topic Modeling (LDA)
        │
        ▼
 Risk Detection
        │
        ▼
 Digital Wellness Index
        │
        ▼
 AI Insights Generation
        │
        ▼
 Streamlit Dashboard
```

---

# Folder Structure

```
DigitalDetoxAnalytics/

│
├── app.py
├── assets/
│   ├── banner.png
│   └── logo.png
│
├── scripts/
│   ├── collect_youtube.py
│   ├── collect_telegram.py
│   ├── collect_bluesky.py
│   ├── collect_twitch.py
│   ├── merge_data.py
│   ├── database.py
│   ├── preprocess.py
│   ├── filter_topic.py
│   ├── feature_engineering.py
│   ├── sentiment_analysis.py
│   ├── topic_modeling.py
│   ├── trend_analysis.py
│   ├── risk_detection.py
│   └── ai_insights.py
│
├── data/
│
├── outputs/
│
├── requirements.txt
├── README.md
└── .streamlit/
```

---

# Features

### Data Engineering

- Multi-platform data collection
- Automated ETL Pipeline
- SQLite Database Integration
- Data Cleaning
- Feature Engineering

---

### Natural Language Processing

- Text Preprocessing
- VADER Sentiment Analysis
- Latent Dirichlet Allocation (LDA)
- Topic Extraction
- Word Cloud Generation

---

### Analytics

- Trend Analysis
- Platform Comparison
- Risk Detection
- AI Generated Insights
- Digital Wellness Index (DWI)

---

### Dashboard

Interactive Streamlit Dashboard including:

- KPI Cards
- Platform Distribution
- Sentiment Analysis
- Topic Distribution
- Risk Distribution
- Monthly Trend
- Word Cloud
- AI Insights
- Platform Comparison
- Project Summary
- Report Download

---

# Technologies Used

| Category | Technology |
|-----------|------------|
| Programming | Python |
| Dashboard | Streamlit |
| Database | SQLite |
| Data Analysis | Pandas |
| Visualization | Plotly |
| Machine Learning | Scikit-learn |
| NLP | NLTK (VADER) |
| Topic Modeling | LDA |
| Word Cloud | WordCloud |

---

# Installation

Clone the repository

```bash
git clone https://github.com/AbhishekAJaiswal/DigitalDetoxAnalytics.git
```

Move to the project folder

```bash
cd DigitalDetoxAnalytics
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the dashboard

```bash
streamlit run app.py
```

---

# Dashboard Preview

Add screenshots here after deployment.

Example:

```
images/dashboard.png
```

---

# Key Results

- Multi-platform social media dataset collected.
- Digital Detox discussions successfully extracted.
- Sentiment classified into Positive, Neutral, and Negative.
- Hidden discussion topics identified using LDA.
- High-risk discussions detected.
- Digital Wellness Index introduced as a custom project metric.
- AI-generated recommendations produced.
- Interactive dashboard created using Streamlit.

---

# Future Scope

- Real-time data streaming.
- Additional social media platforms.
- Transformer-based sentiment models.
- Multilingual topic modeling.
- User-level digital wellbeing prediction.

---

# Team Members

- Aishwarya Manyar
- Abhishek Anand Jaiswal
- Abhinav Kumar
- Aditya Saurabh

---

# Course

Social Media Analytics Capstone

Indian Institute of Technology Jodhpur

---

# License

This project has been developed for academic and educational purposes.