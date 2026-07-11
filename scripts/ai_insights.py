import os
import pandas as pd

print("=" * 70)
print("Digital Detox Analytics - AI Insights Generator")
print("=" * 70)

# -----------------------------------------------------
# Load Dataset
# -----------------------------------------------------

df = pd.read_csv("data/processed/topic_dataset.csv")

print(f"Records Loaded : {len(df)}")

# -----------------------------------------------------
# Create Output Folder
# -----------------------------------------------------

os.makedirs("outputs/insights", exist_ok=True)

# -----------------------------------------------------
# Basic Statistics
# -----------------------------------------------------

total_posts = len(df)

platform_counts = df["platform"].value_counts()

top_platform = platform_counts.idxmax()

top_platform_posts = platform_counts.max()

sentiment_counts = df["sentiment"].value_counts()

dominant_sentiment = sentiment_counts.idxmax()

dominant_sentiment_count = sentiment_counts.max()

topic_counts = df["topic"].value_counts()

dominant_topic = topic_counts.idxmax()

dominant_topic_posts = topic_counts.max()

# -----------------------------------------------------
# Average Engagement
# -----------------------------------------------------

if "engagement_score" in df.columns:

    engagement = (

        df.groupby("platform")["engagement_score"]

        .mean()

        .round(2)

    )

    highest_engagement_platform = engagement.idxmax()

    highest_engagement = engagement.max()

else:

    highest_engagement_platform = "N/A"

    highest_engagement = 0

# -----------------------------------------------------
# Positive Platform
# -----------------------------------------------------

positive = (

    df[df["sentiment"] == "Positive"]

    .groupby("platform")

    .size()

)

if len(positive) > 0:

    positive_platform = positive.idxmax()

else:

    positive_platform = "N/A"

# -----------------------------------------------------
# Negative Platform
# -----------------------------------------------------

negative = (

    df[df["sentiment"] == "Negative"]

    .groupby("platform")

    .size()

)

if len(negative) > 0:

    negative_platform = negative.idxmax()

else:

    negative_platform = "N/A"

# -----------------------------------------------------
# Top Keywords
# -----------------------------------------------------

keywords = (

    df["keyword"]

    .fillna("")

    .str.split(",")

    .explode()

    .str.strip()

)

keywords = keywords[keywords != ""]

top_keywords = keywords.value_counts().head(10)

# -----------------------------------------------------
# AI Insights
# -----------------------------------------------------

insights = []

insights.append("=" * 70)

insights.append("DIGITAL DETOX ANALYTICS")

insights.append("AUTOMATIC INSIGHTS REPORT")

insights.append("=" * 70)

insights.append("")

insights.append(f"Total Social Media Posts Analysed : {total_posts}")

insights.append("")

insights.append("KEY FINDINGS")

insights.append("-" * 40)

insights.append(

    f"• Most active platform : {top_platform} ({top_platform_posts} posts)"

)

insights.append(

    f"• Dominant sentiment : {dominant_sentiment} ({dominant_sentiment_count} posts)"

)

insights.append(

    f"• Most discussed topic : Topic {dominant_topic} ({dominant_topic_posts} posts)"

)

insights.append(

    f"• Highest engagement platform : {highest_engagement_platform}"

)

insights.append(

    f"• Platform with highest positive discussions : {positive_platform}"

)

insights.append(

    f"• Platform with highest negative discussions : {negative_platform}"

)

insights.append("")

insights.append("TOP DIGITAL DETOX KEYWORDS")

insights.append("-" * 40)

for word, count in top_keywords.items():

    insights.append(f"{word} : {count}")

# -----------------------------------------------------
# Recommendations
# -----------------------------------------------------

recommendations = []

recommendations.append("")

recommendations.append("=" * 70)

recommendations.append("AI RECOMMENDATIONS")

recommendations.append("=" * 70)

recommendations.append("")

if dominant_sentiment == "Negative":

    recommendations.append(

        "Increase awareness campaigns promoting digital wellbeing."

    )

else:

    recommendations.append(

        "Positive discussions dominate. Encourage these communities."

    )

if negative_platform != "N/A":

    recommendations.append(

        f"Focus intervention campaigns on {negative_platform}."

    )

if highest_engagement_platform != "N/A":

    recommendations.append(

        f"Use {highest_engagement_platform} for awareness campaigns because of high engagement."

    )

recommendations.append(

    "Promote mindfulness, digital detox and healthy screen habits."

)

recommendations.append(

    "Encourage users to reduce excessive screen time."

)

recommendations.append(

    "Support mental health awareness through online communities."

)

# -----------------------------------------------------
# Save Report
# -----------------------------------------------------

with open(

    "outputs/insights/ai_insights_report.txt",

    "w",

    encoding="utf-8"

) as f:

    for line in insights:

        f.write(line + "\n")

    for line in recommendations:

        f.write(line + "\n")

# -----------------------------------------------------
# Save Summary CSV
# -----------------------------------------------------

summary = pd.DataFrame({

    "Metric":[

        "Total Posts",

        "Most Active Platform",

        "Dominant Sentiment",

        "Dominant Topic",

        "Highest Engagement Platform",

        "Highest Positive Platform",

        "Highest Negative Platform"

    ],

    "Value":[

        total_posts,

        top_platform,

        dominant_sentiment,

        dominant_topic,

        highest_engagement_platform,

        positive_platform,

        negative_platform

    ]

})

summary.to_csv(

    "outputs/insights/project_summary.csv",

    index=False

)

# -----------------------------------------------------
# Console Output
# -----------------------------------------------------

print()

print("=" * 70)

print("AI INSIGHTS GENERATED")

print("=" * 70)

print()

print(summary)

print()

print("Saved Files")

print("--------------------------------")

print("outputs/insights/ai_insights_report.txt")

print("outputs/insights/project_summary.csv")

print()

print("=" * 70)