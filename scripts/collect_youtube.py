from googleapiclient.discovery import build
from dotenv import load_dotenv
import pandas as pd
import os

# --------------------------------------------------
# Load API Key
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("YOUTUBE_API_KEY")

youtube = build(
    "youtube",
    "v3",
    developerKey=api_key
)

# --------------------------------------------------
# Configuration
# --------------------------------------------------

VIDEOS_PER_KEYWORD = 5
COMMENTS_PER_VIDEO = 100

# --------------------------------------------------
# Keywords
# --------------------------------------------------

search_terms = [

    # Digital Detox
    "digital detox",
    "digital wellbeing",
    "digital wellness",
    "digital minimalism",
    "digital habits",

    # Screen Time
    "screen time",
    "reduce screen time",
    "screen addiction",
    "phone addiction",
    "mobile addiction",

    # Social Media
    "social media addiction",
    "social media detox",
    "instagram addiction",
    "facebook addiction",
    "youtube addiction",
    "tiktok addiction",
    "doomscrolling",

    # Productivity
    "productivity",
    "deep work",
    "focus",
    "focus mode",
    "dopamine detox",
    "dopamine fasting",

    # Mental Health
    "mental health",
    "mindfulness",
    "mindfulness meditation",
    "anxiety social media",
    "depression social media",

    # Lifestyle
    "healthy habits",
    "self improvement",
    "self discipline",
    "minimalism",
    "habit building",

    # Technology
    "technology addiction",
    "internet addiction",
    "smartphone addiction",
    "gaming addiction",
    "internet detox",

    # Education
    "study with me",
    "study motivation",
    "student productivity",

    # Sleep
    "sleep hygiene",
    "blue light",
    "sleep and phone",

    # AI
    "AI productivity",
    "AI distraction",
    "digital balance"
]

all_comments = []

# --------------------------------------------------
# Search Videos
# --------------------------------------------------

for keyword in search_terms:

    print("=" * 70)
    print(f"Searching videos for: {keyword}")

    try:

        search_response = youtube.search().list(
            q=keyword,
            part="snippet",
            type="video",
            maxResults=VIDEOS_PER_KEYWORD,
            relevanceLanguage="en"
        ).execute()

    except Exception as e:
        print(e)
        continue

    # --------------------------------------------------

    for item in search_response["items"]:

        video_id = item["id"]["videoId"]

        video_title = item["snippet"]["title"]

        channel = item["snippet"]["channelTitle"]

        published = item["snippet"]["publishedAt"]

        print(f"Collecting comments from: {video_title}")

        try:

            comments = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=COMMENTS_PER_VIDEO,
                textFormat="plainText"
            ).execute()

            for c in comments["items"]:

                snippet = c["snippet"]["topLevelComment"]["snippet"]

                all_comments.append({

                    "platform": "YouTube",

                    "keyword": keyword,

                    "video_id": video_id,

                    "video_title": video_title,

                    "channel_name": channel,

                    "video_published": published,

                    "author": snippet["authorDisplayName"],

                    "comment": snippet["textDisplay"],

                    "likes": snippet["likeCount"],

                    "reply_count": c["snippet"]["totalReplyCount"],

                    "comment_published": snippet["publishedAt"]

                })

        except Exception as e:

            print("Comments Disabled:", e)

# --------------------------------------------------
# DataFrame
# --------------------------------------------------

df = pd.DataFrame(all_comments)

print("\nRemoving duplicate comments...")

df.drop_duplicates(
    subset=["video_id", "author", "comment"],
    inplace=True
)

# --------------------------------------------------

os.makedirs("data/raw", exist_ok=True)

df.to_csv(
    "data/raw/youtube_comments.csv",
    index=False
)

# --------------------------------------------------

print("\n")
print("=" * 70)
print("Collection Finished")
print("=" * 70)

print(f"Total Comments Collected : {len(df)}")

print(f"Unique Videos           : {df['video_id'].nunique()}")

print(f"Unique Channels         : {df['channel_name'].nunique()}")

print("\nSaved to")

print("data/raw/youtube_comments.csv")