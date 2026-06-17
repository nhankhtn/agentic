"""Rule-based UP/DOWN/HOLD forecast model."""

from __future__ import annotations

from typing import Any


def _evidence_key(evidence: dict[str, Any]) -> tuple[str, str]:
    return (str(evidence.get("news_id", "")), str(evidence.get("evidence_text", "")).strip().lower())


def _filter_evidence(
    evidence_list: list[dict[str, Any]],
    exclude: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    if not exclude:
        return list(evidence_list)
    exclude_keys = {_evidence_key(e) for e in exclude}
    return [e for e in evidence_list if _evidence_key(e) not in exclude_keys]


def predict(
    evidence_list: list[dict[str, Any]],
    price_features: dict[str, float],
    ticker: str,
    forecast_time: Any,
    cited_evidence: list[dict[str, Any]] | None = None,
    exclude_evidence: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Predict stock direction from evidence and price features.

    Rule-based score combines sentiment evidence counts with price_5d_return.
    """
    active = _filter_evidence(evidence_list, exclude_evidence)

    positive_count = sum(1 for e in active if e.get("expected_direction") == "UP")
    negative_count = sum(1 for e in active if e.get("expected_direction") == "DOWN")

    price_return = float(price_features.get("price_5d_return", 0.0))
    if price_return > 0:
        positive_count += 0.5
    elif price_return < 0:
        negative_count += 0.5

    total_directional = positive_count + negative_count
    score = positive_count - negative_count

    if score > 0:
        prediction = "UP"
        confidence = positive_count / max(total_directional, 1.0)
        auto_cited = [e for e in active if e.get("expected_direction") == "UP"]
    elif score < 0:
        prediction = "DOWN"
        confidence = negative_count / max(total_directional, 1.0)
        auto_cited = [e for e in active if e.get("expected_direction") == "DOWN"]
    else:
        prediction = "HOLD"
        confidence = 0.5
        auto_cited = active

    final_cited = cited_evidence if cited_evidence is not None else auto_cited
    if exclude_evidence and final_cited:
        final_cited = _filter_evidence(final_cited, exclude_evidence)

    confidence = round(min(max(confidence, 0.0), 1.0), 4)
    rationale = _build_rationale(ticker, prediction, confidence, final_cited, active)

    return {
        "ticker": ticker,
        "forecast_time": forecast_time,
        "prediction": prediction,
        "confidence": confidence,
        "cited_evidence": final_cited,
        "rationale": rationale,
    }


def _build_rationale(
    ticker: str,
    prediction: str,
    confidence: float,
    cited: list[dict[str, Any]],
    all_evidence: list[dict[str, Any]],
) -> str:
    if not all_evidence:
        return (
            f"Dự báo {ticker} {prediction} (confidence={confidence:.2f}) — "
            "không có evidence hợp lệ; fallback từ price features hoặc HOLD."
        )

    if not cited:
        return (
            f"Dự báo {ticker} {prediction} (confidence={confidence:.2f}) — "
            "không có cited evidence rõ ràng."
        )

    parts = [f"'{e.get('evidence_text', '')}'" for e in cited[:3]]
    joined = ", ".join(parts)
    return (
        f"Dự báo {ticker} {prediction} (confidence={confidence:.2f}) dựa trên "
        f"{len(cited)} evidence: {joined}."
    )


def compute_confidence_drop(
    evidence_list: list[dict[str, Any]],
    price_features: dict[str, float],
    ticker: str,
    forecast_time: Any,
    cited_evidence: list[dict[str, Any]],
    cited_evidence_override: list[dict[str, Any]] | None = None,
) -> tuple[float, float, float]:
    """Return (confidence_original, confidence_without, confidence_drop)."""
    cited = cited_evidence_override if cited_evidence_override is not None else cited_evidence

    full = predict(evidence_list, price_features, ticker, forecast_time, cited_evidence=cited)
    without = predict(
        evidence_list,
        price_features,
        ticker,
        forecast_time,
        cited_evidence=cited,
        exclude_evidence=cited,
    )
    original = full["confidence"]
    reduced = without["confidence"]
    return original, reduced, round(original - reduced, 4)
