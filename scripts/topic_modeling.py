import os
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import (
    CountVectorizer,
    TfidfVectorizer,
    ENGLISH_STOP_WORDS
)
from sklearn.decomposition import LatentDirichletAllocation

from wordcloud import WordCloud

print("=" * 70)
print("Digital Detox Analytics - Topic Modeling (LDA)")
print("=" * 70)

# -----------------------------------------------------
# Load Dataset
# -----------------------------------------------------

df = pd.read_csv("data/processed/sentiment_dataset.csv")

print(f"Original Records : {len(df)}")

# -----------------------------------------------------
# Remove Missing Text
# -----------------------------------------------------

df = df.dropna(subset=["clean_text"])

# -----------------------------------------------------
# Keep only English Posts
# -----------------------------------------------------

df = df[
    df["clean_text"].str.contains(r"[a-zA-Z]", regex=True)
]

print(f"English Records : {len(df)}")

documents = df["clean_text"].astype(str)

CUSTOM_STOPWORDS = {

    # -------------------------------------------------
    # English
    # -------------------------------------------------

    "like","im","thing","people","really","know",
    "video","videos","youtube","channel","watch",
    "watching","today","also","would","could",
    "make","made","going","got","get","one","two",
    "time","new","well","use","using","used",
    "see","seen","say","said","still","even",
    "back","much","many","every","always","never",

    # -------------------------------------------------
    # Russian
    # -------------------------------------------------

    "для","по","на","не","мы","вы","это","или",
    "что","как","его","ее","их","они","она",
    "он","бы","же","из","к","ко","от","до",
    "при","если","нет","есть","так","ещё",
    "может","очень","потом","сейчас",

    # -------------------------------------------------
    # Italian
    # -------------------------------------------------

    "di","il","lo","la","gli","le","dei","degli",
    "della","delle","del","dello","al","allo",
    "alla","alle","ai","agli","che","con",
    "per","tra","fra","su","nel","nella",
    "nelle","un","una","uno","sono","era",

    # -------------------------------------------------
    # Spanish
    # -------------------------------------------------

    "de","la","el","los","las","que","para",
    "con","por","una","uno","del","al","como",
    "más","muy","pero","porque","cuando","donde",
    "este","esta","estos","estas",

    # -------------------------------------------------
    # French
    # -------------------------------------------------

    "le","la","les","de","des","du","un","une",
    "et","pour","dans","sur","avec","est","être",
    "au","aux","ce","cette","ces",

    # -------------------------------------------------
    # German
    # -------------------------------------------------

    "der","die","das","und","mit","für","von",
    "den","dem","ein","eine","einer","eines",
    "ist","sind","war","werden","zu","im","am",

    # -------------------------------------------------
    # Portuguese
    # -------------------------------------------------

    "de","da","do","das","dos","para","com",
    "uma","um","que","como","por","mais",
    "muito","não","sim","foi","ser",

    # -------------------------------------------------
    # URLs
    # -------------------------------------------------

    "http","https","www","com"
}

STOPWORDS = ENGLISH_STOP_WORDS.union(CUSTOM_STOPWORDS)

# -----------------------------------------------------
# Vectorization
# -----------------------------------------------------

vectorizer = CountVectorizer(

    stop_words=list(STOPWORDS),

    max_df=0.90,

    min_df=8,

    ngram_range=(1,2)

)

dtm = vectorizer.fit_transform(documents)

# -----------------------------------------------------
# LDA
# -----------------------------------------------------

NUM_TOPICS = 6

lda = LatentDirichletAllocation(

    n_components=NUM_TOPICS,

    random_state=42,

    learning_method="batch",

    max_iter=20

)

lda.fit(dtm)

# -----------------------------------------------------
# Topic Keywords
# -----------------------------------------------------

feature_names = vectorizer.get_feature_names_out()

topics = []

print("\nDetected Topics\n")

for index, topic in enumerate(lda.components_):

    words = [

        feature_names[i]

        for i in topic.argsort()[:-11:-1]

    ]

    print(f"Topic {index+1}")

    print(", ".join(words))

    print()

    topics.append({

        "Topic": f"Topic {index+1}",

        "Keywords": ", ".join(words)

    })

# -----------------------------------------------------
# Save Topic Keywords
# -----------------------------------------------------

os.makedirs("outputs/topics", exist_ok=True)

topic_df = pd.DataFrame(topics)

topic_df.to_csv(

    "outputs/topics/topic_keywords.csv",

    index=False

)

# -----------------------------------------------------
# Assign Topic
# -----------------------------------------------------

topic_values = lda.transform(dtm)

df["topic"] = topic_values.argmax(axis=1) + 1

df.to_csv(

    "data/processed/topic_dataset.csv",

    index=False

)

# -----------------------------------------------------
# TF-IDF Keywords
# -----------------------------------------------------

print("Calculating TF-IDF...")

tfidf = TfidfVectorizer(

    stop_words=list(STOPWORDS),

    max_features=100

)

tfidf_matrix = tfidf.fit_transform(documents)

keywords = pd.DataFrame({

    "Keyword": tfidf.get_feature_names_out(),

    "Score": tfidf_matrix.sum(axis=0).A1

})

keywords = keywords.sort_values(

    "Score",

    ascending=False

)

keywords.to_csv(

    "outputs/topics/tfidf_keywords.csv",

    index=False

)

# -----------------------------------------------------
# Topic Distribution
# -----------------------------------------------------

distribution = (

    df["topic"]

    .value_counts()

    .sort_index()

)

distribution.to_csv(

    "outputs/topics/topic_distribution.csv"

)

plt.figure(figsize=(8,5))

distribution.plot(

    kind="bar"

)

plt.title("Topic Distribution")

plt.xlabel("Topic")

plt.ylabel("Number of Posts")

plt.tight_layout()

plt.savefig(

    "outputs/topics/topic_distribution.png"

)

plt.close()

# -----------------------------------------------------
# Word Cloud
# -----------------------------------------------------

all_text = " ".join(documents)

wc = WordCloud(

    width=1400,

    height=700,

    background_color="white"

).generate(all_text)

plt.figure(figsize=(14,7))

plt.imshow(wc)

plt.axis("off")

plt.tight_layout()

plt.savefig(

    "outputs/topics/topic_wordcloud.png"

)

plt.close()

# -----------------------------------------------------
# Summary
# -----------------------------------------------------

print("=" * 70)

print("Topic Modeling Completed Successfully")

print("=" * 70)

print(f"Total Documents : {len(df)}")

print(f"Topics Created  : {NUM_TOPICS}")

print("\nSaved Files")

print("✔ data/processed/topic_dataset.csv")
print("✔ outputs/topics/topic_keywords.csv")
print("✔ outputs/topics/tfidf_keywords.csv")
print("✔ outputs/topics/topic_distribution.csv")
print("✔ outputs/topics/topic_distribution.png")
print("✔ outputs/topics/topic_wordcloud.png")

print("\nModel Perplexity :", round(lda.perplexity(dtm),2))

print("=" * 70)