"""Unit tests for faithfulness metrics."""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from faithfulness_metrics import (
    classify_verdict,
    compute_confidence_drop,
    evidence_support,
    evaluate_faithfulness,
    temporal_validity,
)
from forecast_model import predict


def _evidence(direction: str, news_id: str = "N1", news_time: str = "2025-03-11 08:00") -> dict:
    return {
        "news_id": news_id,
        "news_time": datetime.strptime(news_time, "%Y-%m-%d %H:%M"),
        "evidence_text": f"sample {direction.lower()} evidence",
        "polarity": "positive" if direction == "UP" else "negative" if direction == "DOWN" else "neutral",
        "expected_direction": direction,
        "confidence": 0.8,
    }


def test_tm01_confidence_drop_zero_without_cited_evidence():
    evidence = [_evidence("DOWN")]
    result = predict(evidence, {"price_5d_return": -0.02}, "TSLA", "2025-03-12 09:00", cited_evidence=[])
    faith = evaluate_faithfulness(
        evidence,
        {"price_5d_return": -0.02},
        "TSLA",
        "2025-03-12 09:00",
        result,
    )
    assert faith["confidence_drop"] == 0.0


def test_tm02_temporal_validity_all_before_forecast():
    cited = [_evidence("DOWN", news_time="2025-03-11 08:00")]
    score = temporal_validity(cited, "2025-03-12 09:00")
    assert score == 1.0


def test_tm03_temporal_validity_below_one_with_future_evidence():
    cited = [
        _evidence("DOWN", news_id="N1", news_time="2025-03-11 08:00"),
        _evidence("DOWN", news_id="N2", news_time="2025-03-12 10:00"),
    ]
    score = temporal_validity(cited, "2025-03-12 09:00")
    assert score == 0.5


def test_tm04_evidence_support_all_aligned():
    cited = [_evidence("UP"), _evidence("UP", news_id="N2")]
    score = evidence_support(cited, "UP")
    assert score == 1.0


def test_tm05_evidence_support_all_opposite():
    cited = [_evidence("DOWN"), _evidence("DOWN", news_id="N2")]
    score = evidence_support(cited, "UP")
    assert score == 0.0


def test_confidence_drop_increases_when_cited_evidence_removed():
    evidence = [_evidence("DOWN"), _evidence("DOWN", news_id="N2")]
    cited = [evidence[0]]
    original, without, drop = compute_confidence_drop(
        evidence,
        {"price_5d_return": -0.03},
        "TSLA",
        "2025-03-12 09:00",
        cited,
    )
    assert original >= without
    assert drop >= 0.0
    assert classify_verdict(drop) in {"likely_faithful", "uncertain", "possibly_decorative"}
