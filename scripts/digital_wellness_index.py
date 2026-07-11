import os
import pandas as pd
import numpy as np

print("=" * 70)
print("Digital Detox Analytics - Digital Wellness Index")
print("=" * 70)

# -----------------------------------------------------
# Load Dataset
# -----------------------------------------------------

df = pd.read_csv("data/processed/topic_dataset.csv")

print(f"Records Loaded : {len(df)}")

# -----------------------------------------------------
# Fill Missing Values
# -----------------------------------------------------

df["clean_text"] = df["clean_text"].fillna("").astype(str)

if "engagement_score" not in df.columns:
    df["engagement_score"] = 0

df["engagement_score"] = df["engagement_score"].fillna(0)

# -----------------------------------------------------
# Wellness Keywords
# -----------------------------------------------------

WELLNESS_KEYWORDS = [

    "digital detox",
    "mindfulness",
    "meditation",
    "exercise",
    "fitness",
    "healthy",
    "health",
    "wellbeing",
    "wellness",
    "reading",
    "books",
    "nature",
    "offline",
    "family",
    "friends",
    "focus",
    "productivity",
    "deep work",
    "sleep",
    "self care",
    "gratitude",
    "happiness",
    "calm",
    "relax",
    "balance",
    "minimalism",
    "digital minimalism",
    "walking",
    "journal",
    "study",
    "learning",
    "dopamine detox"

]

# -----------------------------------------------------
# Risk Keywords
# -----------------------------------------------------

RISK_KEYWORDS = [

    "phone addiction",
    "smartphone addiction",
    "screen addiction",
    "social media addiction",
    "technology addiction",
    "internet addiction",
    "gaming addiction",
    "doomscrolling",
    "burnout",
    "stress",
    "anxiety",
    "depression",
    "lonely",
    "isolation",
    "panic",
    "fear",
    "suicide",
    "can't sleep",
    "insomnia",
    "addicted",
    "compulsive",
    "distraction",
    "procrastination",
    "fatigue"

]

# -----------------------------------------------------
# Sentiment Score
# -----------------------------------------------------

def sentiment_score(sentiment):

    sentiment = str(sentiment).lower()

    if sentiment == "positive":
        return 1.0

    elif sentiment == "neutral":
        return 0.60

    elif sentiment == "negative":
        return 0.20

    return 0.50

df["sentiment_value"] = df["sentiment"].apply(sentiment_score)

# -----------------------------------------------------
# Engagement Normalization
# -----------------------------------------------------

maximum = df["engagement_score"].max()

if maximum == 0:

    df["engagement_normalized"] = 0

else:

    df["engagement_normalized"] = (

        df["engagement_score"] / maximum

    )

# -----------------------------------------------------
# Wellness Bonus
# -----------------------------------------------------

def wellness_bonus(text):

    text = text.lower()

    score = 0

    for keyword in WELLNESS_KEYWORDS:

        if keyword in text:

            score += 1

    return min(score * 3, 30)

df["wellness_bonus"] = df["clean_text"].apply(

    wellness_bonus

)

# -----------------------------------------------------
# Risk Penalty
# -----------------------------------------------------

def risk_penalty(text):

    text = text.lower()

    score = 0

    for keyword in RISK_KEYWORDS:

        if keyword in text:

            score += 1

    return min(score * 4, 35)

df["risk_penalty"] = df["clean_text"].apply(

    risk_penalty

)

# -----------------------------------------------------
# Topic Importance
# -----------------------------------------------------

HIGH_PRIORITY_TOPICS = [1, 2]

MEDIUM_PRIORITY_TOPICS = [3, 4]

def topic_bonus(topic):

    if topic in HIGH_PRIORITY_TOPICS:

        return 10

    elif topic in MEDIUM_PRIORITY_TOPICS:

        return 5

    else:

        return 2

df["topic_bonus"] = df["topic"].apply(topic_bonus)

# -----------------------------------------------------
# Digital Wellness Index
# -----------------------------------------------------

df["digital_wellness_index"] = (

      df["sentiment_value"] * 50

    + df["engagement_normalized"] * 15

    + df["wellness_bonus"]

    + df["topic_bonus"]

    - df["risk_penalty"]

)

df["digital_wellness_index"] = np.clip(

    df["digital_wellness_index"],

    0,

    100

)

df["digital_wellness_index"] = df[

    "digital_wellness_index"

].round(2)

# -----------------------------------------------------
# Wellness Category
# -----------------------------------------------------

def wellness_category(score):

    if score >= 85:
        return "Excellent"

    elif score >= 70:
        return "Good"

    elif score >= 50:
        return "Moderate"

    elif score >= 30:
        return "Needs Improvement"

    return "Critical"

df["wellness_category"] = df[
    "digital_wellness_index"
].apply(wellness_category)

# -----------------------------------------------------
# Dataset Statistics
# -----------------------------------------------------

average_dwi = round(
    df["digital_wellness_index"].mean(), 2
)

maximum_dwi = round(
    df["digital_wellness_index"].max(), 2
)

minimum_dwi = round(
    df["digital_wellness_index"].min(), 2
)

print("\nAverage Digital Wellness Index :", average_dwi)

print("Highest Score :", maximum_dwi)

print("Lowest Score :", minimum_dwi)

# -----------------------------------------------------
# Category Distribution
# -----------------------------------------------------

category_distribution = (

    df["wellness_category"]

    .value_counts()

)

print("\nWellness Category Distribution\n")

print(category_distribution)

# -----------------------------------------------------
# Platform Statistics
# -----------------------------------------------------

platform_statistics = (

    df.groupby("platform")[

        "digital_wellness_index"

    ]

    .agg(

        [

            "count",

            "mean",

            "min",

            "max"

        ]

    )

)

platform_statistics.columns = [

    "Posts",

    "Average_DWI",

    "Minimum_DWI",

    "Maximum_DWI"

]

platform_statistics = platform_statistics.round(2)

print("\nPlatform Statistics\n")

print(platform_statistics)

# -----------------------------------------------------
# Sentiment Statistics
# -----------------------------------------------------

sentiment_statistics = (

    df.groupby("sentiment")[

        "digital_wellness_index"

    ]

    .mean()

)

sentiment_statistics = sentiment_statistics.round(2)

print("\nAverage DWI by Sentiment\n")

print(sentiment_statistics)

# -----------------------------------------------------
# Save Output Folder
# -----------------------------------------------------

os.makedirs(

    "outputs/digital_wellness",

    exist_ok=True

)

# -----------------------------------------------------
# Save Main Dataset
# -----------------------------------------------------

df.to_csv(

    "data/processed/digital_wellness_dataset.csv",

    index=False

)

# -----------------------------------------------------
# Save Statistics
# -----------------------------------------------------

platform_statistics.to_csv(

    "outputs/digital_wellness/platform_statistics.csv"

)

category_distribution.to_csv(

    "outputs/digital_wellness/wellness_distribution.csv"

)

sentiment_statistics.to_csv(

    "outputs/digital_wellness/sentiment_statistics.csv"

)

print("\nDatasets Saved Successfully")

print("data/processed/digital_wellness_dataset.csv")

print("outputs/digital_wellness/platform_statistics.csv")

print("outputs/digital_wellness/wellness_distribution.csv")

print("outputs/digital_wellness/sentiment_statistics.csv")