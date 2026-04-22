import pandas as pd
import re

# ── 1. Load the labMT lexicon ──────────────────────────────────────────────
labmt = pd.read_csv(
    "data/raw/Data_Set_S1.txt",
    sep="\t", skiprows=3,
    usecols=["word", "happiness_average"],
    na_values="--"
)
labmt = labmt.dropna(subset=["happiness_average"])
labmt["word"] = labmt["word"].str.lower().str.strip()
happiness = dict(zip(labmt["word"], labmt["happiness_average"]))
print(f"Loaded {len(happiness)} words from labMT")

# ── 2. Load speeches ───────────────────────────────────────────────────────
df = pd.read_csv("data/processed/speeches.csv")
print(f"Loaded {len(df)} speeches")

# ── 3. Score each speech ───────────────────────────────────────────────────
def score_text(text):
    if not isinstance(text, str):
        return None, 0, 0
    words = re.findall(r"[a-z]+", text.lower())
    matched = [w for w in words if w in happiness]
    if len(matched) == 0:
        return None, len(words), 0
    score = sum(happiness[w] for w in matched) / len(matched)
    coverage = len(matched) / len(words) if words else 0
    return score, len(words), coverage

df[["score", "word_count", "coverage"]] = df["text"].apply(
    lambda t: pd.Series(score_text(t))
)

print(f"Scored {df['score'].notna().sum()} speeches")
print(df[["country", "year", "score", "coverage"]].head(10))

# ── 4. Save ────────────────────────────────────────────────────────────────
df.drop(columns=["text"]).to_csv("data/processed/speeches_scored.csv", index=False)
print("\nSaved to data/processed/speeches_scored.csv")
