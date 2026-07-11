import sqlite3
import pandas as pd
import os

print("=" * 70)
print("Digital Detox Analytics - SQLite Database Pipeline")
print("=" * 70)

# -----------------------------------------------------
# Create database folder
# -----------------------------------------------------

os.makedirs("database", exist_ok=True)

db_path = "database/social_media.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# -----------------------------------------------------
# Load CSV Files
# -----------------------------------------------------

youtube = pd.read_csv("data/raw/youtube_comments.csv")
telegram = pd.read_csv("data/raw/telegram_raw.csv")
bluesky = pd.read_csv("data/raw/bluesky_posts.csv")
twitch = pd.read_csv("data/raw/twitch_relevant.csv")
merged = pd.read_csv("data/processed/merged_dataset.csv")

# -----------------------------------------------------
# Store into SQLite
# -----------------------------------------------------

youtube.to_sql(
    "youtube",
    conn,
    if_exists="replace",
    index=False
)

telegram.to_sql(
    "telegram",
    conn,
    if_exists="replace",
    index=False
)

bluesky.to_sql(
    "bluesky",
    conn,
    if_exists="replace",
    index=False
)

twitch.to_sql(
    "twitch",
    conn,
    if_exists="replace",
    index=False
)

merged.to_sql(
    "merged_dataset",
    conn,
    if_exists="replace",
    index=False
)

# -----------------------------------------------------
# Verify Tables
# -----------------------------------------------------

tables = [
    "youtube",
    "telegram",
    "bluesky",
    "twitch",
    "merged_dataset"
]

print("\nDatabase Summary")
print("-" * 70)

for table in tables:

    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]

    print(f"{table:<18} : {count}")

# -----------------------------------------------------
# Sample Query
# -----------------------------------------------------

print("\nTop Platforms")

query = """

SELECT
platform,
COUNT(*) AS Total_Records

FROM merged_dataset

GROUP BY platform

ORDER BY Total_Records DESC;

"""

result = pd.read_sql(query, conn)

print(result)

# -----------------------------------------------------
# Close Connection
# -----------------------------------------------------

conn.commit()
conn.close()

print("\n" + "=" * 70)
print("SQLite Database Created Successfully")
print("=" * 70)

print(f"\nDatabase Location : {db_path}")