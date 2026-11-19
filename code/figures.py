"""Minimal data-driven redraws of the main numerical panels (not native PDF replicas)."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from recompute import FAMILIES, HAZARDS, GROUPS, CODES, main

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results"
COLORS = ["#a15a30", "#20766f", "#335b88", "#72516e"]
plt.rcParams.update({"font.size": 10, "pdf.fonttype": 42})


def read(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def save(fig, name):
    fig.savefig(OUT / (name + ".pdf"), bbox_inches="tight")
    plt.close(fig)


def draw():
    main()
    rows = read(OUT / "method-family-period.csv")
    periods = list(dict.fromkeys(r["period"] for r in rows))
    fig, ax = plt.subplots(figsize=(8, 4))
    for family, color in zip(FAMILIES, COLORS):
        series = [r for r in rows if r["family"] == family]
        ax.plot(periods, [100*float(r["share"]) for r in series], "o-", label=family, color=color)
    ax.set(ylabel="Papers mentioning a family (%)", ylim=(0, 100))
    ax.legend(fontsize=8)
    save(fig, "method-family-period")
    rows = read(OUT / "strict-hazard-method.csv")
    values = np.array([[100*float(next(r["share"] for r in rows if r["hazard"] == h and r["family"] == f))
                        for f in FAMILIES] for h in HAZARDS])
    fig, ax = plt.subplots(figsize=(10, 4.5))
    img = ax.imshow(values, vmin=0, vmax=100, cmap="Blues")
    ax.set_xticks(range(4), FAMILIES, rotation=15, ha="right")
    ax.set_yticks(range(6), HAZARDS)
    for i in range(6):
        for j in range(4):
            ax.text(j, i, f"{values[i,j]:.0f}%", ha="center", va="center",
                    color="white" if values[i,j] > 55 else "#193242")
    fig.colorbar(img, ax=ax, label="Method-family mentions (%)")
    save(fig, "hazard-method")
    rows = read(OUT / "figure10-source.csv")
    groups = GROUPS + ["All cases"]
    values = [[int(next(r["n"] for r in rows if r["task_group"] == g and r["code"] == c)) for c in CODES] for g in groups]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.imshow(values, cmap="Blues")
    ax.set_xticks(range(6), ["Chronological", "Random", "Order unclear", "Cross-validation", "Unreported", "Unverified"], rotation=15, ha="right")
    ax.set_yticks(range(5), groups)
    for i, group in enumerate(groups):
        denominator = next(r["denominator"] for r in rows if r["task_group"] == group)
        for j, n in enumerate(values[i]):
            ax.text(j, i, f"{n}/{denominator}", ha="center", va="center", color="white" if n > 8 else "black")
    save(fig, "task-validation")
    rows = read(ROOT / "data/target-intervals.csv")
    fig, ax = plt.subplots(figsize=(9, 7))
    for i, row in enumerate(rows):
        x = [float(v) for v in row["hours"].split(";")]
        conditional = row["kind"] == "conditional"
        ax.scatter(x, [i]*len(x), facecolors="none" if conditional else "#335b88", edgecolors="#335b88")
    ax.set_yticks(range(len(rows)), [f'Case {r["case"]}: {r["label"]}' for r in rows])
    ax.set_xscale("log")
    ax.set_xlabel("Reported target interval (hours); open circles: conditional / simulated")
    ax.invert_yaxis()
    save(fig, "target-intervals")


if __name__ == "__main__":
    draw()
