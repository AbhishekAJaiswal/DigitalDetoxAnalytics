import pandas as pd
import os

# Load datasets
youtube = pd.read_csv("data/raw/youtube_comments.csv")
telegram = pd.read_csv("data/raw/telegram_raw.csv")

print(f"YouTube Records : {len(youtube)}")
print(f"Telegram Records : {len(telegram)}")

# -----------------------
# Standardize YouTube
# -----------------------

youtube = youtube.rename(columns={
    "text": "content"
})

youtube["platform"] = "YouTube"

youtube = youtube[[
    "platform",
    "content",
    "author",
    "likes",
    "published_at"
]]

# -----------------------
# Standardize Telegram
# -----------------------

telegram = telegram.rename(columns={
    "text": "content",
    "date": "published_at",
    "views": "likes"
})

telegram["platform"] = "Telegram"

if "author" not in telegram.columns:
    telegram["author"] = "Telegram User"

telegram = telegram[[
    "platform",
    "content",
    "author",
    "likes",
    "published_at"
]]

# -----------------------
# Merge
# -----------------------

merged = pd.concat(
    [youtube, telegram],
    ignore_index=True
)

print("\nTotal Records :", len(merged))

os.makedirs("data/processed", exist_ok=True)

merged.to_csv(
    "data/processed/merged_dataset.csv",
    index=False
)

print("\nMerged dataset saved successfully!")