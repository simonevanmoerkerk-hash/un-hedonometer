import pandas as pd
import matplotlib.pyplot as plt

# ── 1. Load data ───────────────────────────────────────────────────────────
df = pd.read_csv("data/processed/speeches_scored.csv")
df = df.dropna(subset=["score"])

# Note: CHN before 1972 was Taiwan (ROC), not the PRC
df = df[df["year"] >= 1972]
china = df[df["country"] == "CHN"]
usa = df[df["country"] == "USA"]

print(f"China speeches: {len(china)} ({china['year'].min()}–{china['year'].max()})")
print(f"USA speeches:   {len(usa)} ({usa['year'].min()}–{usa['year'].max()})")

# ── 2. Yearly scores ───────────────────────────────────────────────────────
china_yearly = china.groupby("year")["score"].mean()
usa_yearly = usa.groupby("year")["score"].mean()

# ── 3. Plot ────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(china_yearly.index, china_yearly.values,
        color="#DE2910", linewidth=2.5, label="China (PRC)")
ax.plot(usa_yearly.index, usa_yearly.values,
        color="#003087", linewidth=2.5, linestyle="--", label="United States")

# Key historical events relevant to China-US relations
events = {
    1989: "Tiananmen",
    1991: "USSR\ncollapses",
    2001: "9/11\nattacks",
    2001: "China\njoins WTO",
    2003: "Iraq\nWar",
    2008: "Beijing\nOlympics",
    2017: "Trump\ntakes office",
    2020: "COVID-19",
}

for year, label in events.items():
    ax.axvline(x=year, color="gray", linewidth=0.8, linestyle=":")
    ax.text(year + 0.3, 5.63, label, fontsize=7, color="gray", rotation=90, va="top")

ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Mean Happiness Score (labMT, 1–9)", fontsize=12)
ax.set_title("Emotional Tone of UN General Debate Speeches:\nChina (PRC) vs United States (1972–2025)", fontsize=13)
ax.legend(fontsize=11)
ax.set_ylim(5.2, 5.7)
ax.set_xlim(1972, 2025)
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("figures/china_vs_usa.png", dpi=150)
print("Saved figures/china_vs_usa.png")
plt.show()
