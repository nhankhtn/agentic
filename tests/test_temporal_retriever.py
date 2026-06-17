"""Unit tests for temporal retriever."""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from retriever import filter_news_by_time


def _news(news_id: str, news_time: str) -> dict:
    return {
        "news_id": news_id,
        "news_time": datetime.strptime(news_time, "%Y-%m-%d %H:%M"),
        "news_title": "title",
        "news_text": "text",
    }


def test_tc01_valid_news_one_day_before():
    news = [_news("N1", "2025-03-11 08:00")]
    valid, invalid, count = filter_news_by_time(news, "2025-03-12 09:00")
    assert len(valid) == 1
    assert len(invalid) == 0
    assert count == 0


def test_tc02_future_news_six_hours_after():
    news = [_news("N1", "2025-03-12 15:00")]
    valid, invalid, count = filter_news_by_time(news, "2025-03-12 09:00")
    assert len(valid) == 0
    assert len(invalid) == 1
    assert count == 1


def test_tc03_news_at_exact_forecast_time_is_invalid():
    news = [_news("N1", "2025-03-12 09:00")]
    valid, invalid, count = filter_news_by_time(news, "2025-03-12 09:00")
    assert len(valid) == 0
    assert len(invalid) == 1


def test_tc04_mixed_valid_and_invalid_split():
    news = [
        _news("N1", "2025-03-11 08:00"),
        _news("N2", "2025-03-11 10:00"),
        _news("N3", "2025-03-11 12:00"),
        _news("N4", "2025-03-12 15:00"),
        _news("N5", "2025-03-12 09:00"),
    ]
    valid, invalid, count = filter_news_by_time(news, "2025-03-12 09:00")
    assert len(valid) == 3
    assert len(invalid) == 2
    assert count == 2


def test_tc05_empty_news_list():
    valid, invalid, count = filter_news_by_time([], "2025-03-12 09:00")
    assert valid == []
    assert invalid == []
    assert count == 0


def test_tc06_all_news_are_leakage():
    news = [
        _news("N1", "2025-03-12 09:00"),
        _news("N2", "2025-03-12 12:00"),
    ]
    valid, invalid, count = filter_news_by_time(news, "2025-03-12 09:00")
    assert len(valid) == 0
    assert len(invalid) == 2
    assert count == 2
