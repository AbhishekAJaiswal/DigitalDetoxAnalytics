from atproto import Client
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

username = os.getenv("BLUESKY_USERNAME")
password = os.getenv("BLUESKY_PASSWORD")

client = Client()

print("Connecting to Bluesky...")
client.login(username, password)

print("Searching posts...")

keywords = [
    "digital detox",
    "phone addiction",
    "screen time",
    "doomscrolling",
    "social media addiction",
    "digital wellbeing"
    
    # Screen Time
    "screen time",
    "screen addiction",
    "phone addiction",
    "smartphone addiction",
    "mobile addiction",

    # Social Media
    "social media",
    "social media addiction",
    "social media detox",
    "instagram",
    "facebook",
    "youtube",
    "tiktok",
    "reddit",
    "doomscrolling",

    # Productivity
    "productivity",
    "deep work",
    "focus",
    "study",
    "time management",

    # Mental Health
    "mental health",
    "mindfulness",
    "meditation",
    "stress",
    "anxiety",
    "depression",

    # Lifestyle
    "healthy habits",
    "sleep",
    "dopamine detox",
    "internet addiction",

    # AI
    "AI productivity",
    "technology addiction"
]

posts = []

for keyword in keywords:
    print(f"Searching: {keyword}")

    result = client.app.bsky.feed.search_posts(
        params={
            "q": keyword,
            "limit": 25
        }
    )

    for post in result.posts:
        posts.append({
            "platform": "Bluesky",
            "keyword": keyword,
            "author": post.author.handle,
            "text": post.record.text,
            "likes": post.like_count,
            "reposts": post.repost_count,
            "replies": post.reply_count,
            "created_at": post.indexed_at
        })

df = pd.DataFrame(posts)

print(df.head())

os.makedirs("data/raw", exist_ok=True)

df.to_csv("data/raw/bluesky_posts.csv", index=False)

print(f"\nCollected {len(df)} posts.")
print("Bluesky dataset saved successfully!")