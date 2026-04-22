import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter

# ── 1. Load labMT lexicon ──────────────────────────────────────────────────
labmt = pd.read_csv(
    "data/raw/Data_Set_S1.txt",
    sep="\t", skiprows=3,
    usecols=["word", "happiness_average"],
    na_values="--"
)
labmt = labmt.dropna(subset=["happiness_average"])
labmt["word"] = labmt["word"].str.lower().str.strip()
known_words = set(labmt["word"].tolist())

# ── 2. Load speeches ───────────────────────────────────────────────────────
df = pd.read_csv("data/processed/speeches.csv")
china = df[df["country"] == "CHN"]
usa = df[df["country"] == "USA"]

# ── 3. Find OOV words ──────────────────────────────────────────────────────
def get_oov_words(speeches):
    oov = Counter()
    for text in speeches:
        if not isinstance(text, str):
            continue
        words = re.findall(r"[a-z]+", text.lower())
        for w in words:
            if w not in known_words and len(w) > 4:  # skip very short words
                oov[w] += 1
    return oov

china_oov = get_oov_words(china["text"])
usa_oov = get_oov_words(usa["text"])

# Top 20 OOV words for each country
print("Top 20 OOV words in China's speeches:")
for word, count in china_oov.most_common(20):
    print(f"  {word}: {count}")

print("\nTop 20 OOV words in USA's speeches:")
for word, count in usa_oov.most_common(20):
    print(f"  {word}: {count}")

# ── 4. Coverage by country and decade ─────────────────────────────────────
scored = pd.read_csv("data/processed/speeches_scored.csv")

# Add decade column
scored["decade"] = (scored["year"] // 10) * 10

china_scored = scored[scored["country"] == "CHN"]
usa_scored = scored[scored["country"] == "USA"]

china_coverage = china_scored.groupby("decade")["coverage"].mean()
usa_coverage = usa_scored.groupby("decade")["coverage"].mean()

print(f"\nChina mean coverage: {china_scored['coverage'].mean():.3f}")
print(f"USA mean coverage:   {usa_scored['coverage'].mean():.3f}")

# ── 5. Plot coverage by decade ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))

x = range(len(china_coverage))
width = 0.35

bars1 = ax.bar([i - width/2 for i in x], china_coverage.values,
               width, label="China (PRC)", color="#DE2910", alpha=0.75)
bars2 = ax.bar([i + width/2 for i in x], usa_coverage.values,
               width, label="United States", color="#003087", alpha=0.75)

ax.set_xticks(list(x))
ax.set_xticklabels([f"{d}s" for d in china_coverage.index])
ax.set_xlabel("Decade", fontsize=11)
ax.set_ylabel("Mean Coverage (matched words / total words)", fontsize=11)
ax.set_title("labMT Lexicon Coverage by Decade:\nChina (PRC) vs United States", fontsize=12)
ax.legend(fontsize=10)
ax.set_ylim(0.8, 1.0)
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("figures/coverage_by_decade.png", dpi=150)
print("\nSaved figures/coverage_by_decade.png")
plt.show()

# ── 6. Plot top OOV words ──────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# China OOV
china_top = china_oov.most_common(15)
china_words = [x[0] for x in china_top]
china_counts = [x[1] for x in china_top]
ax1.barh(china_words[::-1], china_counts[::-1], color="#DE2910", alpha=0.75)
ax1.set_xlabel("Frequency", fontsize=10)
ax1.set_title("China — Top 15 Words\nNot in labMT Lexicon", fontsize=11)
ax1.grid(axis="x", alpha=0.3)

# USA OOV
usa_top = usa_oov.most_common(15)
usa_words = [x[0] for x in usa_top]
usa_counts = [x[1] for x in usa_top]
ax2.barh(usa_words[::-1], usa_counts[::-1], color="#003087", alpha=0.75)
ax2.set_xlabel("Frequency", fontsize=10)
ax2.set_title("USA — Top 15 Words\nNot in labMT Lexicon", fontsize=11)
ax2.grid(axis="x", alpha=0.3)

fig.suptitle("Most Frequent Out-of-Vocabulary (OOV) Words by Country",
             fontsize=13, y=1.02)

plt.tight_layout()
plt.savefig("figures/oov_words.png", dpi=150, bbox_inches="tight")
print("Saved figures/oov_words.png")
plt.show()
