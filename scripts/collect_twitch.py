import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

# ------------------------------------------------
# Authenticate
# ------------------------------------------------

auth = requests.post(
    "https://id.twitch.tv/oauth2/token",
    params={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
)

token = auth.json()["access_token"]

headers = {
    "Client-ID": CLIENT_ID,
    "Authorization": f"Bearer {token}"
}

print("✅ Connected to Twitch!")

# ------------------------------------------------
# Search Queries
# ------------------------------------------------

queries = [
    "productivity",
    "education",
    "study",
    "mental health",
    "wellness",
    "technology",
    "science",
    "focus",
    "self improvement",
    "digital"
    
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

results = []

for query in queries:

    print(f"\nSearching: {query}")

    response = requests.get(
        "https://api.twitch.tv/helix/search/channels",
        headers=headers,
        params={
            "query": query,
            "first": 20
        }
    )

    if response.status_code != 200:
        print("Error:", response.status_code)
        continue

    channels = response.json()["data"]

    for ch in channels:

        title = ch.get("title", "")
        broadcaster = ch.get("broadcaster_login", "")

        results.append({
            "platform": "Twitch",
            "keyword": query,
            "channel": ch.get("display_name"),
            "broadcaster": broadcaster,
            "title": title,
            "language": ch.get("broadcaster_language"),
            "game": ch.get("game_name"),
            "is_live": ch.get("is_live"),
            "followers": ch.get("followers", ""),
            "thumbnail": ch.get("thumbnail_url")
        })

df = pd.DataFrame(results)

df.drop_duplicates(inplace=True)

os.makedirs("data/raw", exist_ok=True)

df.to_csv("data/raw/twitch_relevant.csv", index=False)

print("\n--------------------------------")
print(df.head())
print("--------------------------------")

print(f"\nCollected {len(df)} relevant Twitch channels.")
print("Saved to data/raw/twitch_relevant.csv")