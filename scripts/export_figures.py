"""Export static figures for report and submission."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "outputs"
FIG_DIR = OUTPUT_DIR / "figures"


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    pred = pd.read_csv(OUTPUT_DIR / "prediction_results.csv")
    faith = pd.read_csv(OUTPUT_DIR / "faithfulness_results.csv")

    # prediction_distribution.png
    counts = pred["prediction"].value_counts()
    plt.figure(figsize=(8, 5))
    counts.plot(kind="bar", color=["#2ecc71", "#e74c3c", "#f1c40f"])
    plt.title("Prediction Distribution")
    plt.xlabel("Prediction")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "prediction_distribution.png", dpi=120)
    plt.close()

    # confidence_drop.png
    plt.figure(figsize=(10, 5))
    plt.bar(faith["ticker"] + " " + faith["forecast_time"].str[-5:], faith["confidence_drop"])
    plt.xticks(rotation=45, ha="right")
    plt.title("Confidence Drop by Forecast")
    plt.ylabel("Confidence Drop")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "confidence_drop.png", dpi=120)
    plt.close()

    # temporal_leakage_warning.png
    leak = faith[faith["leakage_count"] > 0]
    plt.figure(figsize=(8, 4))
    if len(leak):
        plt.bar(leak["ticker"], leak["leakage_count"], color="#e67e22")
        plt.title("Temporal Leakage Warnings by Ticker")
    else:
        plt.text(0.5, 0.5, "No leakage rows", ha="center", va="center")
        plt.title("Temporal Leakage Monitor")
    plt.ylabel("Leakage Count")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "temporal_leakage_warning.png", dpi=120)
    plt.close()

    # faithfulness_radar.png (3 core metrics)
    metrics = {
        "Temporal Validity": faith["temporal_validity"].mean(),
        "Evidence Support": faith["evidence_support"].mean(),
        "Confidence Drop": faith["confidence_drop"].mean(),
    }
    labels = list(metrics.keys())
    values = list(metrics.values())
    values += values[:1]
    angles = [n / float(len(labels)) * 2 * 3.14159 for n in range(len(labels))]
    angles += angles[:1]

    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.2)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    plt.title("Faithfulness Radar (Averages)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "faithfulness_radar.png", dpi=120)
    plt.close()

    print(f"Exported figures to {FIG_DIR}")


if __name__ == "__main__":
    main()
