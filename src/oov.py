import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter

# ── Load labMT lexicon ─────────────────────────────────────────────────────
labmt = pd.read_csv(
    "data/raw/Data_Set_S1.txt",
    sep="\t", skiprows=3,
    usecols=["word", "happiness_average"],
    na_values="--"
)
labmt = labmt.dropna(subset=["happiness_average"])
labmt["word"] = labmt["word"].str.lower().str.strip()
known_words = set(labmt["word"].tolist())

# ── Load speeches ──────────────────────────────────────────────────────────
df = pd.read_csv("data/processed/speeches.csv")
china = df[df["country"] == "CHN"]
usa = df[df["country"] == "USA"]

# ── Find OOV words ─────────────────────────────────────────────────────────
def get_oov_words(speeches):
    oov = Counter()
    for text in speeches:
        if not isinstance(text, str):
            continue
        words = re.findall(r"[a-z]+", text.lower())
        for w in words:
            if w not in known_words and len(w) > 4:
                oov[w] += 1
    return oov

china_oov = get_oov_words(china["text"])
usa_oov = get_oov_words(usa["text"])

print("Top 20 OOV words in China's speeches:")
for word, count in china_oov.most_common(20):
    print(f"  {word}: {count}")

print("\nTop 20 OOV words in USA's speeches:")
for word, count in usa_oov.most_common(20):
    print(f"  {word}: {count}")

# ── Plot ───────────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

china_top = china_oov.most_common(15)
china_words = [x[0] for x in china_top]
china_counts = [x[1] for x in china_top]
ax1.barh(china_words[::-1], china_counts[::-1], color="#DE2910", alpha=0.75)
ax1.set_xlabel("Frequency", fontsize=10)
ax1.set_title("China — Top 15 Words\nNot in labMT Lexicon", fontsize=11)
ax1.grid(axis="x", alpha=0.3)

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
