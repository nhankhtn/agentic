"""Faithfulness metrics for evidence-centric forecasting."""

from __future__ import annotations

import random
from typing import Any

from data_utils import parse_datetime
from forecast_model import compute_confidence_drop, predict


def temporal_validity(cited_evidence: list[dict[str, Any]], forecast_time: Any) -> float:
    """Fraction of cited evidence published before forecast_time."""
    if not cited_evidence:
        return 0.0
    ft = parse_datetime(forecast_time)
    valid = sum(1 for e in cited_evidence if parse_datetime(e["news_time"]) < ft)
    return round(valid / len(cited_evidence), 4)


def evidence_support(cited_evidence: list[dict[str, Any]], prediction: str) -> float:
    """Average alignment between cited evidence direction and prediction."""
    if not cited_evidence:
        return 0.0
    scores = [1.0 if e.get("expected_direction") == prediction else 0.0 for e in cited_evidence]
    return round(sum(scores) / len(scores), 4)


def classify_verdict(confidence_drop: float) -> str:
    if confidence_drop > 0.10:
        return "likely_faithful"
    if confidence_drop < 0.05:
        return "possibly_decorative"
    return "uncertain"


def _random_non_cited(evidence_list: list[dict[str, Any]], cited: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cited_ids = {e.get("news_id") for e in cited}
    pool = [e for e in evidence_list if e.get("news_id") not in cited_ids]
    if not pool:
        return []
    return [random.choice(pool)]


def evaluate_faithfulness(
    evidence_list: list[dict[str, Any]],
    price_features: dict[str, float],
    ticker: str,
    forecast_time: Any,
    prediction_result: dict[str, Any],
    leakage_count: int = 0,
    counter_evidence: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Compute all basic faithfulness metrics for one forecast group."""
    prediction = prediction_result["prediction"]
    cited = prediction_result.get("cited_evidence", [])

    conf_orig, conf_without, drop = compute_confidence_drop(
        evidence_list,
        price_features,
        ticker,
        forecast_time,
        cited,
    )

    random_exclude = _random_non_cited(evidence_list, cited)
    drop_random = 0.0
    if random_exclude:
        full = predict(evidence_list, price_features, ticker, forecast_time, cited_evidence=cited)
        reduced = predict(
            evidence_list,
            price_features,
            ticker,
            forecast_time,
            cited_evidence=cited,
            exclude_evidence=random_exclude,
        )
        drop_random = round(full["confidence"] - reduced["confidence"], 4)

    counter = counter_evidence or []
    has_counter = len(counter) > 0

    return {
        "ticker": ticker,
        "forecast_time": forecast_time,
        "prediction": prediction,
        "confidence_original": conf_orig,
        "confidence_without": conf_without,
        "confidence_drop": drop,
        "confidence_drop_random": drop_random,
        "temporal_validity": temporal_validity(cited, forecast_time),
        "evidence_support": evidence_support(cited, prediction),
        "leakage_count": leakage_count,
        "counterevidence_detected": has_counter,
        "faithful_verdict": classify_verdict(drop),
    }
