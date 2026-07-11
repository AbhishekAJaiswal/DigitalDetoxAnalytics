import subprocess
import sys
import time

print("=" * 70)
print("DIGITAL DETOX ANALYTICS - ETL PIPELINE")
print("=" * 70)

# -----------------------------------------------------
# ETL Scripts
# -----------------------------------------------------

scripts = [

    "scripts/merge_data.py",

    "scripts/database.py",

    "scripts/preprocess.py",

    "scripts/filter_topic.py",

    "scripts/feature_engineering.py",

    "scripts/sentiment_analysis.py"

]

# -----------------------------------------------------
# Execute Pipeline
# -----------------------------------------------------

for script in scripts:

    print("\n" + "=" * 70)
    print(f"Running: {script}")
    print("=" * 70)

    result = subprocess.run(
        [sys.executable, script],
        text=True
    )

    if result.returncode == 0:

        print(f"\n✅ Completed : {script}")

    else:

        print(f"\n❌ ERROR in : {script}")
        print("\nPipeline Stopped.")
        break

    time.sleep(2)

# -----------------------------------------------------
# Pipeline Finished
# -----------------------------------------------------

print("\n" + "=" * 70)
print("ETL PIPELINE EXECUTED SUCCESSFULLY")
print("=" * 70)

print("""
Pipeline Steps Completed:

✔ Merge Dataset
✔ SQLite Database
✔ Data Preprocessing
✔ Topic Filtering
✔ Feature Engineering
✔ Sentiment Analysis

Ready for:
✔ Topic Modeling (LDA)
✔ Streamlit Dashboard
✔ Final Report
""")