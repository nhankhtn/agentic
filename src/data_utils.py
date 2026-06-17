"""Load CSV dataset and group rows by (ticker, forecast_time)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd

VALID_LABELS = {"UP", "DOWN", "HOLD"}
DATETIME_COLS = ("forecast_time", "news_time")


def parse_datetime(value: str | datetime) -> datetime:
    """Parse ISO-like datetime strings used in the dataset."""
    if isinstance(value, datetime):
        return value
    text = str(value).strip()
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return pd.to_datetime(text).to_pydatetime()


def load_csv(path: str) -> pd.DataFrame:
    """Load and validate the news-price dataset."""
    df = pd.read_csv(path)
    required = {
        "ticker",
        "forecast_time",
        "news_id",
        "news_time",
        "news_title",
        "news_text",
        "price_5d_return",
        "label",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    for col in DATETIME_COLS:
        df[col] = df[col].apply(parse_datetime)

    invalid_labels = set(df["label"].unique()) - VALID_LABELS
    if invalid_labels:
        raise ValueError(f"Invalid labels: {invalid_labels}")

    if "volume_change" not in df.columns:
        df["volume_change"] = 0.0

    df = df.dropna(subset=["ticker", "forecast_time", "news_id", "news_time", "news_text", "label"])
    return df


def group_by_forecast(df: pd.DataFrame) -> list[dict[str, Any]]:
    """Group flat CSV rows into forecast units for the pipeline."""
    groups: list[dict[str, Any]] = []
    grouped = df.groupby(["ticker", "forecast_time"], sort=False)

    for (ticker, forecast_time), chunk in grouped:
        first = chunk.iloc[0]
        news_items = []
        for _, row in chunk.iterrows():
            news_items.append(
                {
                    "news_id": row["news_id"],
                    "news_time": row["news_time"],
                    "news_title": row["news_title"],
                    "news_text": row["news_text"],
                }
            )

        groups.append(
            {
                "ticker": ticker,
                "forecast_time": forecast_time,
                "news": news_items,
                "price_features": {
                    "price_5d_return": float(first["price_5d_return"]),
                    "volume_change": float(first["volume_change"]),
                },
                "label": first["label"],
            }
        )

    return groups


def dataset_statistics(df: pd.DataFrame) -> dict[str, Any]:
    """Summary stats for reports and validation."""
    groups = group_by_forecast(df)
    leakage_rows = 0
    for group in groups:
        ft = group["forecast_time"]
        for news in group["news"]:
            if news["news_time"] >= ft:
                leakage_rows += 1

    label_counts = df.drop_duplicates(["ticker", "forecast_time"])["label"].value_counts().to_dict()
    return {
        "total_rows": len(df),
        "forecast_groups": len(groups),
        "tickers": sorted(df["ticker"].unique().tolist()),
        "label_distribution": label_counts,
        "temporal_leakage_rows": leakage_rows,
    }
