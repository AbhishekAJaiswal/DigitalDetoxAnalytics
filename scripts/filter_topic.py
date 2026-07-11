import pandas as pd
import os

print("=" * 60)
print("Digital Detox Analytics - Topic Filtering")
print("=" * 60)

# -----------------------------------------------------
# Load Cleaned Dataset
# -----------------------------------------------------

df = pd.read_csv("data/cleaned/cleaned_dataset.csv")

print(f"Original Records : {len(df)}")

# -----------------------------------------------------
# Digital Detox Keywords
# -----------------------------------------------------

KEYWORDS = [

    "digital detox",
    "digital wellbeing",
    "digital wellness",
    "digital minimalism",
    "screen time",
    "screen addiction",
    "phone addiction",
    "mobile addiction",
    "smartphone addiction",
    "social media",
    "social media addiction",
    "social media detox",
    "instagram",
    "facebook",
    "youtube",
    "reddit",
    "telegram",
    "tiktok",
    "doomscrolling",
    "technology addiction",
    "internet addiction",
    "productivity",
    "deep work",
    "focus",
    "focus mode",
    "mindfulness",
    "meditation",
    "mental health",
    "stress",
    "anxiety",
    "depression",
    "healthy habits",
    "self improvement",
    "sleep",
    "blue light",
    "dopamine",
    "dopamine detox",
    "study",
    "gaming addiction"
]

# -----------------------------------------------------
# Filter Function
# -----------------------------------------------------

def is_relevant(text):

    text = str(text).lower()

    return any(keyword in text for keyword in KEYWORDS)

# -----------------------------------------------------
# Filter Dataset
# -----------------------------------------------------

filtered_df = df[df["clean_text"].apply(is_relevant)]

# -----------------------------------------------------
# Remove Duplicates
# -----------------------------------------------------

filtered_df.drop_duplicates(
    subset=["platform", "author", "clean_text"],
    inplace=True
)

# -----------------------------------------------------
# Save
# -----------------------------------------------------

os.makedirs("data/processed", exist_ok=True)

filtered_df.to_csv(
    "data/processed/digital_detox_dataset.csv",
    index=False
)

# -----------------------------------------------------

print(f"Filtered Records : {len(filtered_df)}")
print(f"Removed Records  : {len(df) - len(filtered_df)}")

print("\nPlatform Distribution:\n")
print(filtered_df["platform"].value_counts())

print("\nSaved to:")
print("data/processed/digital_detox_dataset.csv")

print("=" * 60)
print("Topic Filtering Completed")
print("=" * 60)