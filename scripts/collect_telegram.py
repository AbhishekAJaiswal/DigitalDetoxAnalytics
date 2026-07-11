from telethon.sync import TelegramClient
from dotenv import load_dotenv
import pandas as pd
import os

# -----------------------------
# Load Environment Variables
# -----------------------------

load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

client = TelegramClient(
    "digital_detox_session",
    api_id,
    api_hash
)

client.start()

print("=" * 70)
print("Connected to Telegram")
print("=" * 70)

# -------------------------------------------------
# Channels
# -------------------------------------------------

channels = [

    "tips",
    "telegram",

    "Quiterrapp",
    "detox_social_media",
    "socialmediadetox",

    "mentalhealthcenter",
    "mentalhealthcenter_chat"

]

# -------------------------------------------------
# Keywords
# -------------------------------------------------

FILTER_KEYWORDS = [

    "digital detox",
    "digital wellbeing",
    "digital wellness",
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
    "mental health",
    "mindfulness",
    "meditation",
    "stress",
    "anxiety",
    "depression",
    "healthy habits",
    "self improvement",
    "minimalism",
    "sleep",
    "blue light",
    "dopamine",
    "dopamine detox",
    "study",
    "study motivation",
    "gaming addiction",
    "distressed",
    "depression",
    "addiction"
]

all_messages = []

# -------------------------------------------------
# Collect Messages
# -------------------------------------------------

for channel in channels:

    print("\n" + "=" * 70)
    print(f"Collecting from : {channel}")

    try:

        entity = client.get_entity(channel)

        count = 0

        for message in client.iter_messages(entity, limit=5000):

            if not message.message:
                continue

            text = message.message

            matched = []

            for keyword in FILTER_KEYWORDS:

                if keyword.lower() in text.lower():

                    matched.append(keyword)

            all_messages.append({

                "platform": "Telegram",
                "channel": channel,
                "message_id": message.id,
                "date": message.date,
                "keyword": ", ".join(matched),
                "text": text,
                "views": message.views if message.views else 0,
                "forwards": getattr(message, "forwards", 0),
                "message_length": len(text)

            })

            count += 1

            if count % 500 == 0:
                print(f"{count} messages collected...")

        print(f"Finished : {count} messages")

    except Exception as e:

        print(f"Skipped {channel}")
        print(e)

# -------------------------------------------------
# Disconnect
# -------------------------------------------------

client.disconnect()

# -------------------------------------------------
# Save Dataset
# -------------------------------------------------

df = pd.DataFrame(all_messages)

if not df.empty:

    df.drop_duplicates(
        subset=["channel", "message_id"],
        inplace=True
    )

os.makedirs("data/raw", exist_ok=True)

df.to_csv(
    "data/raw/telegram_raw.csv",
    index=False
)

print("\n" + "=" * 70)
print("Telegram Dataset Saved Successfully")
print("=" * 70)

print(f"Total Messages : {len(df)}")
print(f"Channels        : {len(channels)}")
print("Saved : data/raw/telegram_raw.csv")