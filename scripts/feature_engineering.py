import pandas as pd
import os

print("=" * 60)
print("Digital Detox Analytics - Feature Engineering")
print("=" * 60)

# -----------------------------------------------------
# Load Cleaned Dataset
# -----------------------------------------------------

df = pd.read_csv("data/processed/digital_detox_dataset.csv")

print("Records Loaded :", len(df))

# -----------------------------------------------------
# Text Features
# -----------------------------------------------------

df["clean_text"] = df["clean_text"].fillna("")

df["text"] = df["text"].fillna("")

df["keyword"] = df["keyword"].fillna("")

df["text_length"] = df["clean_text"].apply(len)

df["word_count"] = df["clean_text"].apply(
    lambda x: len(x.split())
)

df["sentence_count"] = df["text"].astype(str).apply(
    lambda x: x.count(".") + x.count("!") + x.count("?")
)

df["avg_word_length"] = df.apply(

    lambda row:

    row["text_length"] / row["word_count"]

    if row["word_count"] > 0 else 0,

    axis=1

)

# -----------------------------------------------------
# Keyword Count
# -----------------------------------------------------

df["keyword_count"] = df["keyword"].fillna("").astype(str).apply(

    lambda x: 0 if x == "" else len(x.split(","))

)

# -----------------------------------------------------
# Engagement Score
# -----------------------------------------------------

df["likes"] = pd.to_numeric(

    df["likes"],

    errors="coerce"

).fillna(0)

df["engagement_score"] = df["likes"]

# -----------------------------------------------------
# Date Features
# -----------------------------------------------------

df["date"] = pd.to_datetime(

    df["date"],

    errors="coerce"

)

df["posting_year"] = df["date"].dt.year

df["posting_month"] = df["date"].dt.month

df["posting_day"] = df["date"].dt.day

df["posting_hour"] = df["date"].dt.hour

# -----------------------------------------------------
# Platform Weight
# -----------------------------------------------------

weights = {

    "YouTube":4,

    "Telegram":3,

    "Bluesky":2,

    "Twitch":1

}

df["platform_weight"] = df["platform"].map(weights)

# -----------------------------------------------------
# Save
# -----------------------------------------------------

os.makedirs(

    "data/processed",

    exist_ok=True

)

df.to_csv(

    "data/processed/feature_dataset.csv",

    index=False

)

print()

print("Feature Dataset Saved")

print()

print(df.head())

print()

print("=" * 60)

print("Feature Engineering Completed")

print("=" * 60)