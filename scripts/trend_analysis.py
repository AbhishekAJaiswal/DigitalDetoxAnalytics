import os
import pandas as pd
import matplotlib.pyplot as plt

print("=" * 70)
print("Digital Detox Analytics - Trend Analysis")
print("=" * 70)

# -----------------------------------------------------
# Load Dataset
# -----------------------------------------------------

df = pd.read_csv("data/processed/topic_dataset.csv")

print(f"Records Loaded : {len(df)}")

# -----------------------------------------------------
# Create Output Folder
# -----------------------------------------------------

os.makedirs("outputs/trends", exist_ok=True)

# -----------------------------------------------------
# Convert Date
# -----------------------------------------------------

df["date"] = pd.to_datetime(df["date"], errors="coerce")

df["year_month"] = df["date"].dt.to_period("M").astype(str)

# -----------------------------------------------------
# Platform Distribution
# -----------------------------------------------------

platform_counts = df["platform"].value_counts()

platform_counts.to_csv(
    "outputs/trends/platform_distribution.csv"
)

plt.figure(figsize=(8,5))

platform_counts.plot(kind="bar")

plt.title("Platform Distribution")

plt.xlabel("Platform")

plt.ylabel("Posts")

plt.tight_layout()

plt.savefig(
    "outputs/trends/platform_distribution.png"
)

plt.close()

# -----------------------------------------------------
# Sentiment Distribution
# -----------------------------------------------------

sentiment_counts = df["sentiment"].value_counts()

sentiment_counts.to_csv(
    "outputs/trends/sentiment_distribution.csv"
)

plt.figure(figsize=(8,5))

sentiment_counts.plot(kind="bar")

plt.title("Sentiment Distribution")

plt.xlabel("Sentiment")

plt.ylabel("Posts")

plt.tight_layout()

plt.savefig(
    "outputs/trends/sentiment_distribution.png"
)

plt.close()

# -----------------------------------------------------
# Topic Distribution
# -----------------------------------------------------

topic_counts = df["topic"].value_counts().sort_index()

topic_counts.to_csv(
    "outputs/trends/topic_distribution.csv"
)

plt.figure(figsize=(8,5))

topic_counts.plot(kind="bar")

plt.title("Topic Distribution")

plt.xlabel("Topic")

plt.ylabel("Posts")

plt.tight_layout()

plt.savefig(
    "outputs/trends/topic_distribution.png"
)

plt.close()

# -----------------------------------------------------
# Monthly Trend
# -----------------------------------------------------

monthly_posts = (

    df.groupby("year_month")

    .size()

)

monthly_posts.to_csv(
    "outputs/trends/monthly_posts.csv"
)

plt.figure(figsize=(10,5))

monthly_posts.plot(marker="o")

plt.title("Monthly Digital Detox Discussions")

plt.xlabel("Month")

plt.ylabel("Posts")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "outputs/trends/monthly_posts.png"
)

plt.close()

# -----------------------------------------------------
# Engagement by Platform
# -----------------------------------------------------

if "engagement_score" in df.columns:

    engagement = (

        df.groupby("platform")["engagement_score"]

        .mean()

        .round(2)

    )

else:

    engagement = pd.Series()

engagement.to_csv(
    "outputs/trends/engagement_by_platform.csv"
)

if not engagement.empty:

    plt.figure(figsize=(8,5))

    engagement.plot(kind="bar")

    plt.title("Average Engagement by Platform")

    plt.xlabel("Platform")

    plt.ylabel("Average Engagement")

    plt.tight_layout()

    plt.savefig(
        "outputs/trends/engagement_by_platform.png"
    )

    plt.close()

# -----------------------------------------------------
# Top Keywords
# -----------------------------------------------------

keyword_counts = (

    df["keyword"]

    .fillna("")

    .str.split(",")

    .explode()

    .str.strip()

)

keyword_counts = keyword_counts[keyword_counts != ""]

keyword_counts = keyword_counts.value_counts().head(20)

keyword_counts.to_csv(
    "outputs/trends/top_keywords.csv"
)

plt.figure(figsize=(10,6))

keyword_counts.sort_values().plot(kind="barh")

plt.title("Top Keywords")

plt.tight_layout()

plt.savefig(
    "outputs/trends/top_keywords.png"
)

plt.close()

# -----------------------------------------------------
# Summary Report
# -----------------------------------------------------

summary = []

summary.append("=" * 60)
summary.append("DIGITAL DETOX ANALYTICS SUMMARY")
summary.append("=" * 60)
summary.append(f"Total Posts : {len(df)}")
summary.append(f"Platforms : {df['platform'].nunique()}")
summary.append(f"Topics : {df['topic'].nunique()}")

summary.append("")

summary.append(
    f"Most Active Platform : {platform_counts.idxmax()}"
)

summary.append(
    f"Most Common Sentiment : {sentiment_counts.idxmax()}"
)

summary.append(
    f"Dominant Topic : Topic {topic_counts.idxmax()}"
)

if not engagement.empty:

    summary.append(

        f"Highest Engagement Platform : {engagement.idxmax()}"

    )

summary.append("")

summary.append("Platform Distribution")

summary.append(platform_counts.to_string())

summary.append("")

summary.append("Sentiment Distribution")

summary.append(sentiment_counts.to_string())

summary.append("")

summary.append("Topic Distribution")

summary.append(topic_counts.to_string())

with open(

    "outputs/trends/summary_report.txt",

    "w",

    encoding="utf-8"

) as f:

    f.write("\n".join(summary))

# -----------------------------------------------------

print("\nTrend Analysis Completed Successfully")

print("\nFiles Generated")

print("-------------------------------------------")

for file in sorted(os.listdir("outputs/trends")):

    print(file)

print("\nSummary Report Created")

print("outputs/trends/summary_report.txt")

print("=" * 70)