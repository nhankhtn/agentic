"""Rule-based evidence extraction from financial news text."""

from __future__ import annotations

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

NEGATIVE_KEYWORDS = [
    "miss",
    "misses",
    "weak",
    "decline",
    "declines",
    "drop",
    "loss",
    "recall",
    "layoff",
    "fine",
    "lawsuit",
    "shortage",
    "cut",
    "downgrade",
    "slump",
    "concern",
    "risk",
    "warning",
    "disappointing",
    "disruption",
]

POSITIVE_KEYWORDS = [
    "beat",
    "beats",
    "strong",
    "growth",
    "launch",
    "launches",
    "surge",
    "profit",
    "record",
    "partnership",
    "innovation",
    "upgrade",
    "exceed",
    "outperform",
    "rise",
    "rally",
    "boost",
]

NEUTRAL_KEYWORDS = [
    "meeting",
    "announce",
    "maintain",
    "hold",
    "review",
    "explore",
    "consider",
    "discuss",
    "schedule",
    "report",
]


def _count_keywords(text: str, keywords: list[str]) -> int:
    lowered = text.lower()
    return sum(1 for kw in keywords if re.search(rf"\b{re.escape(kw)}\b", lowered))


def _snippet_around_keyword(text: str, keyword: str, window: int = 40) -> str:
    lowered = text.lower()
    idx = lowered.find(keyword.lower())
    if idx < 0:
        return text[:80].strip()
    start = max(0, idx - window)
    end = min(len(text), idx + len(keyword) + window)
    snippet = text[start:end].strip()
    return snippet


def extract_evidence_from_news(news: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract evidence items from a single news record."""
    text = f"{news.get('news_title', '')} {news.get('news_text', '')}".strip()
    news_id = news["news_id"]
    news_time = news["news_time"]

    if len(text.split()) < 10:
        logger.warning("Short news text for %s — defaulting to neutral", news_id)
        return [
            {
                "news_id": news_id,
                "news_time": news_time,
                "evidence_text": text[:80],
                "polarity": "neutral",
                "expected_direction": "HOLD",
                "confidence": 0.3,
            }
        ]

    neg = _count_keywords(text, NEGATIVE_KEYWORDS)
    pos = _count_keywords(text, POSITIVE_KEYWORDS)

    evidence_list: list[dict[str, Any]] = []

    if neg > 0:
        kw = next(k for k in NEGATIVE_KEYWORDS if re.search(rf"\b{re.escape(k)}\b", text.lower()))
        evidence_list.append(
            {
                "news_id": news_id,
                "news_time": news_time,
                "evidence_text": _snippet_around_keyword(text, kw),
                "polarity": "negative",
                "expected_direction": "DOWN",
                "confidence": round(neg / (neg + pos + 1), 2),
            }
        )

    if pos > 0:
        kw = next(k for k in POSITIVE_KEYWORDS if re.search(rf"\b{re.escape(k)}\b", text.lower()))
        evidence_list.append(
            {
                "news_id": news_id,
                "news_time": news_time,
                "evidence_text": _snippet_around_keyword(text, kw),
                "polarity": "positive",
                "expected_direction": "UP",
                "confidence": round(pos / (neg + pos + 1), 2),
            }
        )

    if not evidence_list:
        evidence_list.append(
            {
                "news_id": news_id,
                "news_time": news_time,
                "evidence_text": text[:80],
                "polarity": "neutral",
                "expected_direction": "HOLD",
                "confidence": 0.4,
            }
        )

    return evidence_list


def extract_evidence_from_news_list(news_list: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Extract and flatten evidence from multiple news items."""
    all_evidence: list[dict[str, Any]] = []
    for news in news_list:
        all_evidence.extend(extract_evidence_from_news(news))
    return all_evidence
