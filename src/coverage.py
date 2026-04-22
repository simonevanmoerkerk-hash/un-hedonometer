import pandas as pd
import matplotlib.pyplot as plt

# ── Load scored speeches ───────────────────────────────────────────────────
scored = pd.read_csv("data/processed/speeches_scored.csv")

# Add decade column
scored["decade"] = (scored["year"] // 10) * 10

china_scored = scored[scored["country"] == "CHN"]
usa_scored = scored[scored["country"] == "USA"]

print(f"China mean coverage: {china_scored['coverage'].mean():.3f}")
print(f"USA mean coverage:   {usa_scored['coverage'].mean():.3f}")

# ── Average coverage by decade ─────────────────────────────────────────────
china_coverage = china_scored.groupby("decade")["coverage"].mean()
usa_coverage = usa_scored.groupby("decade")["coverage"].mean()

# ── Plot ───────────────────────────────────────────────────────────────────
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
print("Saved figures/coverage_by_decade.png")
plt.show()
