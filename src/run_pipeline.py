"""End-to-end pipeline: CSV -> predictions + faithfulness outputs."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix

SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from data_utils import dataset_statistics, group_by_forecast, load_csv, parse_datetime
from evidence_extractor import extract_evidence_from_news_list
from evidence_selector import select_evidence
from faithfulness_metrics import evaluate_faithfulness
from forecast_model import predict
from retriever import filter_news_by_time

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def process_group(group: dict[str, Any]) -> dict[str, Any]:
    """Run the full ML pipeline for one (ticker, forecast_time) group."""
    ticker = group["ticker"]
    forecast_time = group["forecast_time"]
    price_features = group["price_features"]
    label = group["label"]

    valid_news, invalid_news, leakage_count = filter_news_by_time(group["news"], forecast_time)
    evidence_list = extract_evidence_from_news_list(valid_news)

    if not evidence_list:
        prediction_result = predict([], price_features, ticker, forecast_time, cited_evidence=[])
        selection = {"pro_evidence": [], "counter_evidence": [], "cited_evidence": []}
    else:
        preliminary = predict(evidence_list, price_features, ticker, forecast_time)
        selection = select_evidence(evidence_list, preliminary["prediction"])
        prediction_result = predict(
            evidence_list,
            price_features,
            ticker,
            forecast_time,
            cited_evidence=selection["cited_evidence"],
        )

    faithfulness = evaluate_faithfulness(
        evidence_list,
        price_features,
        ticker,
        forecast_time,
        prediction_result,
        leakage_count=leakage_count,
        counter_evidence=selection["counter_evidence"],
    )

    return {
        "ticker": ticker,
        "forecast_time": forecast_time,
        "label": label,
        "prediction": prediction_result["prediction"],
        "confidence": prediction_result["confidence"],
        "correct": prediction_result["prediction"] == label,
        "rationale": prediction_result["rationale"],
        "cited_evidence": prediction_result["cited_evidence"],
        "pro_evidence": selection["pro_evidence"],
        "counter_evidence": selection["counter_evidence"],
        "valid_news": valid_news,
        "invalid_future_news": invalid_news,
        "leakage_count": leakage_count,
        "faithfulness": faithfulness,
        "evidence_list": evidence_list,
        "price_features": price_features,
    }


def run_pipeline(input_path: str, output_dir: str | Path) -> tuple[pd.DataFrame, pd.DataFrame, list[dict[str, Any]]]:
    """Execute pipeline on a dataset and write CSV outputs."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = load_csv(input_path)
    groups = group_by_forecast(df)
    results: list[dict[str, Any]] = [process_group(g) for g in groups]

    prediction_rows = []
    faithfulness_rows = []

    for r in results:
        ft = parse_datetime(r["forecast_time"]).strftime("%Y-%m-%d %H:%M")
        prediction_rows.append(
            {
                "ticker": r["ticker"],
                "forecast_time": ft,
                "prediction": r["prediction"],
                "confidence": r["confidence"],
                "label": r["label"],
                "correct": r["correct"],
                "rationale": r["rationale"],
                "leakage_count": r["leakage_count"],
            }
        )
        faithfulness_rows.append(
            {
                "ticker": r["faithfulness"]["ticker"],
                "forecast_time": parse_datetime(r["faithfulness"]["forecast_time"]).strftime("%Y-%m-%d %H:%M"),
                "prediction": r["faithfulness"]["prediction"],
                "confidence_original": r["faithfulness"]["confidence_original"],
                "confidence_without": r["faithfulness"]["confidence_without"],
                "confidence_drop": r["faithfulness"]["confidence_drop"],
                "confidence_drop_random": r["faithfulness"]["confidence_drop_random"],
                "temporal_validity": r["faithfulness"]["temporal_validity"],
                "evidence_support": r["faithfulness"]["evidence_support"],
                "faithful_verdict": r["faithfulness"]["faithful_verdict"],
                "leakage_count": r["faithfulness"]["leakage_count"],
                "counterevidence_detected": r["faithfulness"]["counterevidence_detected"],
            }
        )

    pred_df = pd.DataFrame(prediction_rows)
    faith_df = pd.DataFrame(faithfulness_rows)

    pred_path = output_dir / "prediction_results.csv"
    faith_path = output_dir / "faithfulness_results.csv"
    pred_df.to_csv(pred_path, index=False)
    faith_df.to_csv(faith_path, index=False)

    stats = dataset_statistics(df)
    stats_path = output_dir / "dataset_stats.json"
    stats_path.write_text(json.dumps(stats, indent=2), encoding="utf-8")

    y_true = pred_df["label"].tolist()
    y_pred = pred_df["prediction"].tolist()
    accuracy = accuracy_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred, labels=["UP", "DOWN", "HOLD"])
    metrics_summary = {
        "accuracy": round(float(accuracy), 4),
        "confusion_matrix_labels": ["UP", "DOWN", "HOLD"],
        "confusion_matrix": cm.tolist(),
        "mean_confidence_drop": round(float(faith_df["confidence_drop"].mean()), 4),
        "mean_temporal_validity": round(float(faith_df["temporal_validity"].mean()), 4),
        "mean_evidence_support": round(float(faith_df["evidence_support"].mean()), 4),
    }
    (output_dir / "metrics_summary.json").write_text(json.dumps(metrics_summary, indent=2), encoding="utf-8")

    logger.info("Wrote %s (%d rows)", pred_path, len(pred_df))
    logger.info("Wrote %s (%d rows)", faith_path, len(faith_df))
    logger.info("Accuracy: %.2f%%", accuracy * 100)

    return pred_df, faith_df, results


def main() -> None:
    parser = argparse.ArgumentParser(description="Run faithful evidence forecasting pipeline")
    parser.add_argument(
        "--input",
        default=str(PROJECT_ROOT / "data" / "sample_news_price.csv"),
        help="Path to input CSV",
    )
    parser.add_argument(
        "--output-dir",
        default=str(PROJECT_ROOT / "outputs"),
        help="Directory for output CSV files",
    )
    args = parser.parse_args()
    run_pipeline(args.input, args.output_dir)


if __name__ == "__main__":
    main()
