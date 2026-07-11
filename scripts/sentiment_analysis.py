import pandas as pd
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

print("=" * 60)
print("Digital Detox Analytics - Sentiment Analysis")
print("=" * 60)

# -----------------------------------------------------
# Load Dataset
# -----------------------------------------------------

df = pd.read_csv("data/processed/feature_dataset.csv")

print("Records Loaded :", len(df))

# -----------------------------------------------------
# Handle Missing Values
# -----------------------------------------------------

df["clean_text"] = df["clean_text"].fillna("").astype(str)

# -----------------------------------------------------
# Initialize VADER
# -----------------------------------------------------

analyzer = SentimentIntensityAnalyzer()

# -----------------------------------------------------
# Calculate Sentiment Scores
# -----------------------------------------------------

df["positive"] = df["clean_text"].apply(
    lambda x: analyzer.polarity_scores(x)["pos"]
)

df["negative"] = df["clean_text"].apply(
    lambda x: analyzer.polarity_scores(x)["neg"]
)

df["neutral"] = df["clean_text"].apply(
    lambda x: analyzer.polarity_scores(x)["neu"]
)

df["compound"] = df["clean_text"].apply(
    lambda x: analyzer.polarity_scores(x)["compound"]
)

# -----------------------------------------------------
# Sentiment Label
# -----------------------------------------------------

def classify_sentiment(score):

    if score >= 0.05:
        return "Positive"

    elif score <= -0.05:
        return "Negative"

    else:
        return "Neutral"


df["sentiment"] = df["compound"].apply(classify_sentiment)

# -----------------------------------------------------
# Save Dataset
# -----------------------------------------------------

os.makedirs("data/processed", exist_ok=True)

df.to_csv(
    "data/processed/sentiment_dataset.csv",
    index=False
)

# -----------------------------------------------------
# Summary
# -----------------------------------------------------

print("\nSentiment Distribution\n")

print(df["sentiment"].value_counts())

print("\nAverage Compound Score :", round(df["compound"].mean(), 3))

print("\nSaved to : data/processed/sentiment_dataset.csv")

print("=" * 60)
print("Sentiment Analysis Completed")
print("=" * 60)