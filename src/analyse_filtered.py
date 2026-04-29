import pandas as pd
import matplotlib.pyplot as plt
import re

# ── 1. Load labMT lexicon ──────────────────────────────────────────────────
labmt = pd.read_csv(
    "data/raw/Data_Set_S1.txt",
    sep="\t", skiprows=3,
    usecols=["word", "happiness_average"],
    na_values="--"
)
labmt = labmt.dropna(subset=["happiness_average"])
labmt["word"] = labmt["word"].str.lower().str.strip()
happiness = dict(zip(labmt["word"], labmt["happiness_average"]))

# ── 2. Load speeches ───────────────────────────────────────────────────────
df = pd.read_csv("data/processed/speeches.csv")

# ── 3. Score with happiness filter (remove neutral words 4.0–6.0) ─────────
# This is a standard technique in hedonometer research (Dodds et al. 2011)
# By removing neutral words, only emotionally charged words contribute to the score
# This makes differences between groups more visible

FILTER_LOW = 4.0   # words scoring BELOW 4.0 are kept (negative words)
FILTER_HIGH = 6.0  # words scoring ABOVE 6.0 are kept (positive words)
                   # words between 4.0 and 6.0 are removed (neutral zone)

def score_filtered(text):
    if not isinstance(text, str):
        return None, 0
    words = re.findall(r"[a-z]+", text.lower())
    # Only keep words outside the neutral zone (below 4 or above 6)
    matched = [w for w in words if w in happiness and
               (happiness[w] < FILTER_LOW or happiness[w] > FILTER_HIGH)]
    if len(matched) == 0:
        return None, 0
    score = sum(happiness[w] for w in matched) / len(matched)
    return score, len(matched)

df[["score_filtered", "matched_filtered"]] = df["text"].apply(
    lambda t: pd.Series(score_filtered(t))
)

print(f"Scored {df['score_filtered'].notna().sum()} speeches with filter")
print(df[["country", "year", "score_filtered"]].head(10))

# ── 4. Plot ────────────────────────────────────────────────────────────────
china = df[df["country"] == "CHN"]
usa = df[df["country"] == "USA"]

china_yearly = china.groupby("year")["score_filtered"].mean()
usa_yearly = usa.groupby("year")["score_filtered"].mean()

fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(china_yearly.index, china_yearly.values,
        color="#DE2910", linewidth=2.5, label="China (PRC)")
ax.plot(usa_yearly.index, usa_yearly.values,
        color="#003087", linewidth=2.5, linestyle="--", label="United States")

# Same events as Figure 1
events = [
    (1989, "Tiananmen", 0),
    (1991, "USSR\ncollapses", 0),
    (2001, "9/11", 0.04),
    (2001, "China joins\nWTO", -0.04),
    (2008, "Beijing\nOlympics", 0),
    (2012, "Xi takes\npower", 0),
    (2017, "Trump takes\noffice", 0),
    (2020, "COVID-19", 0),
]

for year, label, offset in events:
    ax.axvline(x=year, color="gray", linewidth=0.8, linestyle=":")
    ax.text(year + 0.2, ax.get_ylim()[1] - 0.02 + offset,
            label, fontsize=7, color="gray", rotation=90, va="top")

ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Mean Happiness Score — filtered (labMT, 1–9)", fontsize=12)
ax.set_title("Emotional Tone of UN General Debate Speeches (Neutral Words Removed):\nChina (PRC) vs United States (1972–2025)", fontsize=13)
ax.legend(fontsize=11)
ax.set_xlim(1972, 2025)
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("figures/china_vs_usa_filtered.png", dpi=150)
print("Saved figures/china_vs_usa_filtered.png")
plt.show()