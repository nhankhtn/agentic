"""Select pro, counter, and cited evidence before forecasting."""

from __future__ import annotations

from typing import Any


def _evidence_key(evidence: dict[str, Any]) -> tuple[str, str]:
    return (str(evidence.get("news_id", "")), str(evidence.get("evidence_text", "")).strip().lower())


def _dominant_direction(evidence_list: list[dict[str, Any]]) -> str:
    up = sum(1 for e in evidence_list if e.get("expected_direction") == "UP")
    down = sum(1 for e in evidence_list if e.get("expected_direction") == "DOWN")
    if up > down:
        return "UP"
    if down > up:
        return "DOWN"
    return "HOLD"


def select_evidence(
    all_evidence: list[dict[str, Any]],
    dominant_direction: str | None = None,
    top_k: int = 3,
) -> dict[str, list[dict[str, Any]]]:
    """
    Split evidence into pro, counter, and cited subsets.

    Returns dict with keys: pro_evidence, counter_evidence, cited_evidence
    """
    if not all_evidence:
        return {"pro_evidence": [], "counter_evidence": [], "cited_evidence": []}

    direction = dominant_direction or _dominant_direction(all_evidence)

    seen: set[tuple[str, str]] = set()
    unique: list[dict[str, Any]] = []
    for item in all_evidence:
        key = _evidence_key(item)
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)

    if direction == "UP":
        pro = [e for e in unique if e.get("expected_direction") == "UP"]
        counter = [e for e in unique if e.get("expected_direction") == "DOWN"]
    elif direction == "DOWN":
        pro = [e for e in unique if e.get("expected_direction") == "DOWN"]
        counter = [e for e in unique if e.get("expected_direction") == "UP"]
    else:
        pro = [e for e in unique if e.get("expected_direction") == "HOLD"]
        counter = [e for e in unique if e.get("expected_direction") in ("UP", "DOWN")]

    pro_sorted = sorted(pro, key=lambda e: e.get("confidence", 0), reverse=True)
    cited = pro_sorted[:top_k] if pro_sorted else unique[:1]

    return {
        "pro_evidence": pro_sorted,
        "counter_evidence": counter,
        "cited_evidence": cited,
    }
