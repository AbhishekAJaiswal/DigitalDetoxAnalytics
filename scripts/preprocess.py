import pandas as pd
import re
import string
import os

# -----------------------------------------------------
# Load Dataset
# -----------------------------------------------------

df = pd.read_csv("data/processed/merged_dataset.csv")

print("=" * 60)
print("Digital Detox Analytics - Preprocessing")
print("=" * 60)

print("Original Records :", len(df))

# -----------------------------------------------------
# Remove Duplicates
# -----------------------------------------------------

df.drop_duplicates(inplace=True)

# -----------------------------------------------------
# Remove Empty Text
# -----------------------------------------------------

df.dropna(subset=["text"], inplace=True)

df = df[df["text"].str.strip() != ""]

# -----------------------------------------------------
# Text Cleaning Function
# -----------------------------------------------------

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words("english"))

lemmatizer = WordNetLemmatizer()

def clean_text(text):

    text = str(text).lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove HTML
    text = re.sub(r"<.*?>", "", text)

    # Remove @mentions
    text = re.sub(r"@\w+", "", text)

    # Remove # but keep word
    text = re.sub(r"#", "", text)

    # Remove numbers
    text = re.sub(r"\d+", "", text)

    # Remove punctuation
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Tokenize
    words = text.split()

    # Remove stopwords
    words = [

        word

        for word in words

        if word not in stop_words

    ]

    # Lemmatization
    words = [

        lemmatizer.lemmatize(word)

        for word in words

    ]

    return " ".join(words)

# -----------------------------------------------------
# Apply Cleaning
# -----------------------------------------------------

df["clean_text"] = df["text"].apply(clean_text)

# -----------------------------------------------------
# Save
# -----------------------------------------------------

os.makedirs("data/cleaned", exist_ok=True)

df.to_csv(
    "data/cleaned/cleaned_dataset.csv",
    index=False
)

print("Cleaned Records :", len(df))

print("\nSaved to : data/cleaned/cleaned_dataset.csv")

print("=" * 60)
print("Preprocessing Completed Successfully")
print("=" * 60)