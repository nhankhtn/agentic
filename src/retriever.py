"""Temporal retriever: filter news strictly before forecast_time."""

from __future__ import annotations

import logging
from typing import Any

from data_utils import parse_datetime

logger = logging.getLogger(__name__)


def filter_news_by_time(
    news_list: list[dict[str, Any]],
    forecast_time: str | Any,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], int]:
    """
    Split news into valid (before forecast) and invalid (future/leakage).

    Returns:
        valid_news, invalid_future_news, leakage_count
    """
    ft = parse_datetime(forecast_time)
    valid_news: list[dict[str, Any]] = []
    invalid_future_news: list[dict[str, Any]] = []

    for news in news_list:
        news_time = parse_datetime(news["news_time"])
        if news_time < ft:
            valid_news.append(news)
        else:
            invalid_future_news.append(news)
            logger.warning(
                "[WARNING] Temporal leakage detected: news_id=%s, news_time=%s > forecast_time=%s",
                news.get("news_id"),
                news_time.strftime("%Y-%m-%d %H:%M"),
                ft.strftime("%Y-%m-%d %H:%M"),
            )

    return valid_news, invalid_future_news, len(invalid_future_news)
