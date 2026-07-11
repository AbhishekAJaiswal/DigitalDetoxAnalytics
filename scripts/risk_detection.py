import os
import pandas as pd

print("=" * 70)
print("Digital Detox Analytics - Risk Detection")
print("=" * 70)

# -----------------------------------------------------
# Load Dataset
# -----------------------------------------------------

df = pd.read_csv("data/processed/topic_dataset.csv")

print(f"Records Loaded : {len(df)}")

# -----------------------------------------------------
# Clean Text
# -----------------------------------------------------

df["clean_text"] = df["clean_text"].fillna("").astype(str)

# -----------------------------------------------------
# Risk Keywords
# -----------------------------------------------------

RISK_KEYWORDS = [

    "phone addiction",
    "screen addiction",
    "social media addiction",
    "technology addiction",
    "internet addiction",
    "gaming addiction",
    "doomscrolling",
    "stress",
    "anxiety",
    "depression",
    "burnout",
    "panic",
    "fear",
    "lonely",
    "loneliness",
    "insomnia",
    "cant sleep",
    "can't sleep",
    "suicide",
    "suicidal",
    "tired",
    "fatigue",
    "obsession",
    "compulsive",
    "overthinking"

]

# -----------------------------------------------------
# Wellness Keywords
# -----------------------------------------------------

WELLNESS_KEYWORDS = [

    "digital detox",
    "mindfulness",
    "meditation",
    "exercise",
    "healthy",
    "wellbeing",
    "wellness",
    "reading",
    "books",
    "nature",
    "family",
    "friends",
    "focus",
    "productivity",
    "deep work",
    "sleep",
    "gratitude",
    "balance",
    "self care"

]

# -----------------------------------------------------
# Calculate Risk Score
# -----------------------------------------------------

def calculate_risk(row):

    text = row["clean_text"].lower()

    score = 0

    # ------------------------
    # Sentiment
    # ------------------------

    sentiment = str(row["sentiment"]).lower()

    if sentiment == "negative":
        score += 35

    elif sentiment == "neutral":
        score += 15

    else:
        score += 5

    # ------------------------
    # Risk Keywords
    # ------------------------

    for keyword in RISK_KEYWORDS:

        if keyword in text:
            score += 10

    # ------------------------
    # Wellness Keywords
    # ------------------------

    for keyword in WELLNESS_KEYWORDS:

        if keyword in text:
            score -= 5

    # ------------------------
    # Engagement
    # ------------------------

    if "engagement_score" in row.index:

        engagement = row["engagement_score"]

        if pd.notna(engagement):

            if engagement > 50:
                score += 5

            elif engagement > 100:
                score += 8

    # ------------------------
    # Topic Adjustment
    # ------------------------

    topic = row["topic"]

    if topic in [1,2]:
        score += 5

    elif topic in [5,6]:
        score -= 2

    return max(score,0)

df["risk_score"] = df.apply(

    calculate_risk,

    axis=1

)

# -----------------------------------------------------
# Risk Category
# -----------------------------------------------------

def classify(score):

    if score >= 45:
        return "High"

    elif score >= 25:
        return "Medium"

    return "Low"

df["risk_level"] = df["risk_score"].apply(classify)

# -----------------------------------------------------
# Save Dataset
# -----------------------------------------------------

os.makedirs(

    "outputs/risk",

    exist_ok=True

)

df.to_csv(

    "data/processed/risk_dataset.csv",

    index=False

)

# -----------------------------------------------------
# Statistics
# -----------------------------------------------------

risk_distribution = (

    df["risk_level"]

    .value_counts()

)

risk_distribution.to_csv(

    "outputs/risk/risk_distribution.csv"

)

platform_risk = (

    pd.crosstab(

        df["platform"],

        df["risk_level"]

    )

)

platform_risk.to_csv(

    "outputs/risk/platform_risk.csv"

)

# -----------------------------------------------------
# Console Output
# -----------------------------------------------------

print()

print("Risk Distribution")

print("-----------------------------")

print(risk_distribution)

print()

print("Average Risk Score :",

      round(df["risk_score"].mean(),2))

print()

print("Saved Files")

print("-----------------------------")

print("data/processed/risk_dataset.csv")

print("outputs/risk/risk_distribution.csv")

print("outputs/risk/platform_risk.csv")

print()

print("=" * 70)

print("Risk Detection Completed")

print("=" * 70)