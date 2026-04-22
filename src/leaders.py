import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ── 1. Load data ───────────────────────────────────────────────────────────
df = pd.read_csv("data/processed/speeches_scored.csv")
df = df.dropna(subset=["score"])
df = df[df["year"] >= 1972]

china = df[df["country"] == "CHN"]
usa = df[df["country"] == "USA"]

# ── 2. Define leadership eras ──────────────────────────────────────────────
usa_presidents = [
    (1972, 1977, "Nixon &\nFord"),
    (1977, 1981, "Carter"),
    (1981, 1993, "Reagan &\nBush Sr"),
    (1993, 2001, "Clinton"),
    (2001, 2009, "Bush Jr"),
    (2009, 2017, "Obama"),
    (2017, 2021, "Trump"),
    (2021, 2025, "Biden"),
    (2025, 2026, "Trump II"),
]

china_leaders = [
    (1972, 1978, "Mao &\nHua"),
    (1978, 1989, "Deng\nXiaoping"),
    (1989, 2002, "Jiang\nZemin"),
    (2002, 2012, "Hu\nJintao"),
    (2012, 2026, "Xi\nJinping"),
]

# ── 3. Calculate average score per leader ─────────────────────────────────
def avg_score(country_df, eras):
    results = []
    for start, end, name in eras:
        subset = country_df[
            (country_df["year"] >= start) & (country_df["year"] < end)
        ]
        if len(subset) > 0:
            results.append((name, subset["score"].mean(), len(subset)))
    return results

usa_scores = avg_score(usa, usa_presidents)
china_scores = avg_score(china, china_leaders)

# ── 4. Plot ────────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# USA bar chart
usa_names = [x[0] for x in usa_scores]
usa_vals = [x[1] for x in usa_scores]
bars1 = ax1.barh(usa_names, usa_vals, color="#003087", alpha=0.75)
ax1.set_xlim(5.2, 5.65)
ax1.set_xlabel("Mean Happiness Score (labMT)", fontsize=10)
ax1.set_title("USA — Average Score\nby President", fontsize=12)
ax1.axvline(x=sum(usa_vals)/len(usa_vals), color="gray",
            linewidth=1.5, linestyle="--", label="USA average")
ax1.legend(fontsize=9)
ax1.grid(axis="x", alpha=0.3)
# Add value labels
for bar, val in zip(bars1, usa_vals):
    ax1.text(val + 0.002, bar.get_y() + bar.get_height()/2,
             f"{val:.3f}", va="center", fontsize=9)

# China bar chart
china_names = [x[0] for x in china_scores]
china_vals = [x[1] for x in china_scores]
bars2 = ax2.barh(china_names, china_vals, color="#DE2910", alpha=0.75)
ax2.set_xlim(5.2, 5.65)
ax2.set_xlabel("Mean Happiness Score (labMT)", fontsize=10)
ax2.set_title("China — Average Score\nby Leader", fontsize=12)
ax2.axvline(x=sum(china_vals)/len(china_vals), color="gray",
            linewidth=1.5, linestyle="--", label="China average")
ax2.legend(fontsize=9)
ax2.grid(axis="x", alpha=0.3)
# Add value labels
for bar, val in zip(bars2, china_vals):
    ax2.text(val + 0.002, bar.get_y() + bar.get_height()/2,
             f"{val:.3f}", va="center", fontsize=9)

fig.suptitle("Mean Happiness Score of UN Speeches by Leadership Era (1972–2025)",
             fontsize=13, y=1.02)

plt.tight_layout()
plt.savefig("figures/china_vs_usa_leaders.png", dpi=150, bbox_inches="tight")
print("Saved figures/china_vs_usa_leaders.png")
plt.show()
