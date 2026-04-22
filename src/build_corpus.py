import os
import pandas as pd

# ── Load speeches from speeches_raw folder ─────────────────────────────────
# Source: UN General Debate Corpus (Baturo, Dasandi, Mikhaylov 2017)
# Downloaded from: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/0TJX8Y
# We keep only China (CHN) and USA speeches from 1972 onwards.
# Note: CHN before 1972 represents Republic of China (ROC), not the Public Republic of China (PRC).
# The People's Republic of China joined the UN on October 25, 1971.

# Path to the raw speech files — flat folder with CHN and USA files only
TXT_DIR = "data/raw/speeches_raw"

COUNTRIES = ["CHN", "USA"]
START_YEAR = 1972

# rows will collect each speech as a row of data
rows = []

# Go through each file in the folder
for filename in sorted(os.listdir(TXT_DIR)):

    # Skip anything that isn't a .txt file
    if not filename.endswith(".txt"):
        continue

    # Filenames look like: CHN_26_1972.txt
    # We split by "_" to get country, session, year separately
    parts = filename.replace(".txt", "").split("_")
    if len(parts) < 3:
        continue

    country = parts[0]   # e.g. "CHN"
    year = int(parts[2]) # e.g. 1972

    # Skip any country we don't want, or any year before 1972
    if country not in COUNTRIES or year < START_YEAR:
        continue

    # Open the file and read the full speech text
    filepath = os.path.join(TXT_DIR, filename)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    # Add this speech as a row with country, year, and text
    rows.append({"country": country, "year": year, "text": text})

# Turn the list of rows into a table
df = pd.DataFrame(rows)

# Sort by country and year
df = df.sort_values(["country", "year"]).reset_index(drop=True)

# Print a summary
print(f"Loaded {len(df)} speeches")
print(df.groupby("country")["year"].agg(["min", "max", "count"]))

# Save to processed folder
df.to_csv("data/processed/speeches.csv", index=False)
print("\nSaved to data/processed/speeches.csv")