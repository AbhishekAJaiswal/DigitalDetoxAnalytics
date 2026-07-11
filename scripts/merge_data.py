import pandas as pd
import os

print("=" * 70)
print("Digital Detox Analytics - Data Merge Pipeline")
print("=" * 70)

# -------------------------------------------------------
# Create processed folder
# -------------------------------------------------------

os.makedirs("data/processed", exist_ok=True)

# -------------------------------------------------------
# Load YouTube
# -------------------------------------------------------

print("\nLoading YouTube dataset...")

youtube = pd.read_csv("data/raw/youtube_comments.csv")

youtube = youtube.rename(columns={

    "comment": "text",
    "channel_name": "source",
    "comment_published": "date"

})

youtube["platform"] = "YouTube"

# Keep required columns only

youtube = youtube[[
    "platform",
    "source",
    "author",
    "keyword",
    "text",
    "likes",
    "date"
]]

print(f"YouTube Records : {len(youtube)}")

# -------------------------------------------------------
# Load Telegram
# -------------------------------------------------------

print("\nLoading Telegram dataset...")

telegram = pd.read_csv("data/raw/telegram_raw.csv")

telegram = telegram.rename(columns={

    "channel": "source",
    "text": "text",
    "date": "date"

})

telegram["platform"] = "Telegram"

telegram["author"] = telegram["source"]

telegram["likes"] = 0

telegram["keyword"] = ""

telegram = telegram[[
    "platform",
    "source",
    "author",
    "keyword",
    "text",
    "likes",
    "date"
]]

print(f"Telegram Records : {len(telegram)}")

# -------------------------------------------------------
# Load Bluesky
# -------------------------------------------------------

print("\nLoading Bluesky dataset...")

bluesky = pd.read_csv("data/raw/bluesky_posts.csv")

# Rename according to your CSV columns
# Adjust if required

bluesky = bluesky.rename(columns={

    "author": "author",
    "text": "text",
    "created_at": "date"

})

bluesky["platform"] = "Bluesky"

if "likes" not in bluesky.columns:
    bluesky["likes"] = 0

if "keyword" not in bluesky.columns:
    bluesky["keyword"] = ""

if "source" not in bluesky.columns:
    bluesky["source"] = "Bluesky"

bluesky = bluesky[[
    "platform",
    "source",
    "author",
    "keyword",
    "text",
    "likes",
    "date"
]]

print(f"Bluesky Records : {len(bluesky)}")

# -------------------------------------------------------
# Load Twitch
# -------------------------------------------------------

print("\nLoading Twitch dataset...")

twitch = pd.read_csv("data/raw/twitch_relevant.csv")

print("\nTwitch Columns:")
print(twitch.columns.tolist())

twitch["platform"] = "Twitch"

# Map columns to our standard schema

twitch["source"] = twitch["game"]

# channel contains the streamer/channel name
twitch["author"] = twitch["channel"]

# Keep keyword collected by your script
if "keyword" not in twitch.columns:
    twitch["keyword"] = ""

# Stream title becomes text
twitch["text"] = twitch["title"]

# Followers will act as engagement
twitch["likes"] = twitch["followers"]

# No timestamp available in this dataset
twitch["date"] = ""

twitch = twitch[[
    "platform",
    "source",
    "author",
    "keyword",
    "text",
    "likes",
    "date"
]]

print(f"Twitch Records : {len(twitch)}")

# -------------------------------------------------------
# Merge
# -------------------------------------------------------

print("\nMerging datasets...")

merged = pd.concat(

    [
        youtube,
        telegram,
        bluesky,
        twitch
    ],

    ignore_index=True

)

# -------------------------------------------------------
# Remove duplicates
# -------------------------------------------------------

before = len(merged)

merged.drop_duplicates(

    subset=["platform", "author", "text"],

    inplace=True

)

after = len(merged)

print(f"Duplicates Removed : {before-after}")

# -------------------------------------------------------
# Save
# -------------------------------------------------------

merged.to_csv(

    "data/processed/merged_dataset.csv",

    index=False

)

# -------------------------------------------------------

print("\n" + "=" * 70)

print("MERGE COMPLETED SUCCESSFULLY")

print("=" * 70)

print(f"Total Records : {len(merged)}")

print("\nPlatform Distribution")

print(merged["platform"].value_counts())

print("\nSaved to")

print("data/processed/merged_dataset.csv")