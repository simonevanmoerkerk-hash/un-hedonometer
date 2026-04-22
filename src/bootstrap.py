import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/speeches_scored.csv")
df = df.dropna(subset=["score"])
df = df[df["year"] >= 1972]

china = df[df["country"] == "CHN"]["score"].values
usa = df[df["country"] == "USA"]["score"].values

observed_diff = china.mean() - usa.mean()
print(f"China mean score: {china.mean():.4f}")
print(f"USA mean score:   {usa.mean():.4f}")
print(f"Observed difference (China − USA): {observed_diff:.4f}")

np.random.seed(42)
diffs = []
for _ in range(10000):
    c = np.random.choice(china, size=len(china), replace=True)
    u = np.random.choice(usa, size=len(usa), replace=True)
    diffs.append(c.mean() - u.mean())

diffs = np.array(diffs)
ci_low, ci_high = np.percentile(diffs, [2.5, 97.5])
print(f"95% CI: [{ci_low:.4f}, {ci_high:.4f}]")

fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(diffs, bins=60, color="#DE2910", alpha=0.7, edgecolor="white")
ax.axvline(observed_diff, color="navy", linewidth=2, label=f"Observed diff: {observed_diff:.4f}")
ax.axvline(ci_low, color="gray", linewidth=1.5, linestyle="--", label=f"95% CI: [{ci_low:.4f}, {ci_high:.4f}]")
ax.axvline(ci_high, color="gray", linewidth=1.5, linestyle="--")
ax.axvline(0, color="black", linewidth=1, linestyle=":")
ax.set_xlabel("Difference in Mean Happiness Score (China − USA)", fontsize=11)
ax.set_ylabel("Frequency", fontsize=11)
ax.set_title("Bootstrap Distribution: China vs USA\n(10,000 iterations)", fontsize=12)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig("figures/bootstrap_china_usa.png", dpi=150)
print("Saved figures/bootstrap_china_usa.png")
plt.show()