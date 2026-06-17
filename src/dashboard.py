"""Streamlit dashboard for faithful evidence forecasting."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from data_utils import group_by_forecast, load_csv
from run_pipeline import process_group

DATA_PATH = PROJECT_ROOT / "data" / "sample_news_price.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


@st.cache_data
def load_groups() -> list[dict]:
    df = load_csv(str(DATA_PATH))
    return group_by_forecast(df)


@st.cache_data
def load_output_tables() -> tuple[pd.DataFrame, pd.DataFrame]:
    pred = pd.read_csv(OUTPUT_DIR / "prediction_results.csv")
    faith = pd.read_csv(OUTPUT_DIR / "faithfulness_results.csv")
    return pred, faith


def render_prediction_overview(pred_df: pd.DataFrame) -> None:
    st.subheader("Prediction Overview")
    tickers = ["All"] + sorted(pred_df["ticker"].unique().tolist())
    selected = st.selectbox("Filter by ticker", tickers)
    view = pred_df if selected == "All" else pred_df[pred_df["ticker"] == selected]

    accuracy = view["correct"].mean() if len(view) else 0.0
    c1, c2, c3 = st.columns(3)
    c1.metric("Predictions", len(view))
    c2.metric("Accuracy", f"{accuracy:.1%}")
    c3.metric("Avg Confidence", f"{view['confidence'].mean():.2f}" if len(view) else "0.00")

    st.dataframe(view, use_container_width=True)
    if len(view):
        fig = px.histogram(view, x="prediction", color="prediction", title="Prediction Distribution")
        st.plotly_chart(fig, use_container_width=True)


def render_evidence_explorer(groups: list[dict]) -> None:
    st.subheader("Evidence Explorer")
    options = [f"{g['ticker']} | {g['forecast_time']}" for g in groups]
    choice = st.selectbox("Select forecast", options)
    idx = options.index(choice)
    result = process_group(groups[idx])

    st.write(f"**Prediction:** {result['prediction']} | **Confidence:** {result['confidence']:.2f}")
    st.write(f"**Label:** {result['label']} | **Correct:** {result['correct']}")
    st.info(result["rationale"])

    if result["leakage_count"] > 0:
        st.error(f"Temporal leakage detected: {result['leakage_count']} news item(s) excluded.")

    cited_df = pd.DataFrame(result["cited_evidence"])
    if not cited_df.empty:
        st.write("### Cited Evidence")
        st.dataframe(cited_df, use_container_width=True)

    if result["counter_evidence"]:
        st.write("### Counterevidence")
        st.dataframe(pd.DataFrame(result["counter_evidence"]), use_container_width=True)

    st.write("### Valid News")
    st.dataframe(pd.DataFrame(result["valid_news"]), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Remove cited evidence", type="primary"):
            st.session_state["compare"] = process_group_with_exclusion(groups[idx], exclude_cited=True)
    with col2:
        if st.button("Remove random non-cited evidence"):
            st.session_state["compare"] = process_group_with_exclusion(groups[idx], exclude_random=True)

    if "compare" in st.session_state:
        cmp = st.session_state["compare"]
        st.write("### Confidence Comparison")
        st.json(
            {
                "confidence_original": cmp["confidence_original"],
                "confidence_after_removal": cmp["confidence_after_removal"],
                "confidence_drop": cmp["confidence_drop"],
            }
        )


def process_group_with_exclusion(group: dict, exclude_cited: bool = False, exclude_random: bool = False) -> dict:
    """Re-run forecast with cited or random evidence removed."""
    from evidence_extractor import extract_evidence_from_news_list
    from evidence_selector import select_evidence
    from forecast_model import predict
    from retriever import filter_news_by_time

    valid_news, _, _ = filter_news_by_time(group["news"], group["forecast_time"])
    evidence_list = extract_evidence_from_news_list(valid_news)
    preliminary = predict(evidence_list, group["price_features"], group["ticker"], group["forecast_time"])
    selection = select_evidence(evidence_list, preliminary["prediction"])
    cited = selection["cited_evidence"]

    full = predict(
        evidence_list,
        group["price_features"],
        group["ticker"],
        group["forecast_time"],
        cited_evidence=cited,
    )

    exclude = cited if exclude_cited else []
    if exclude_random and evidence_list:
        cited_ids = {e["news_id"] for e in cited}
        pool = [e for e in evidence_list if e["news_id"] not in cited_ids]
        exclude = [pool[0]] if pool else []

    reduced = predict(
        evidence_list,
        group["price_features"],
        group["ticker"],
        group["forecast_time"],
        cited_evidence=cited,
        exclude_evidence=exclude,
    )

    return {
        "confidence_original": full["confidence"],
        "confidence_after_removal": reduced["confidence"],
        "confidence_drop": round(full["confidence"] - reduced["confidence"], 4),
    }


def render_faithfulness(faith_df: pd.DataFrame) -> None:
    st.subheader("Faithfulness Analysis")
    if faith_df.empty:
        st.warning("No faithfulness results found. Run the pipeline first.")
        return

    fig = px.bar(
        faith_df,
        x="forecast_time",
        y="confidence_drop",
        color="faithful_verdict",
        hover_data=["ticker", "prediction"],
        title="Confidence Drop by Forecast",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(faith_df, use_container_width=True)

    metrics = {
        "Temporal Validity": faith_df["temporal_validity"].mean(),
        "Evidence Support": faith_df["evidence_support"].mean(),
        "Confidence Drop": faith_df["confidence_drop"].mean(),
    }
    if "counterevidence_detected" in faith_df.columns:
        metrics["Counterevidence Coverage"] = faith_df["counterevidence_detected"].mean()

    fig_radar = go.Figure()
    fig_radar.add_trace(
        go.Scatterpolar(
            r=list(metrics.values()),
            theta=list(metrics.keys()),
            fill="toself",
            name="Avg Metrics",
        )
    )
    fig_radar.update_layout(title="Faithfulness Radar (normalized averages)")
    st.plotly_chart(fig_radar, use_container_width=True)


def render_leakage_monitor(groups: list[dict]) -> None:
    st.subheader("Temporal Leakage Monitor")
    rows = []
    for group in groups:
        ft = group["forecast_time"]
        for news in group["news"]:
            if news["news_time"] >= ft:
                delta_hours = (news["news_time"] - ft).total_seconds() / 3600
                rows.append(
                    {
                        "ticker": group["ticker"],
                        "news_id": news["news_id"],
                        "news_time": news["news_time"],
                        "forecast_time": ft,
                        "delta_hours": round(delta_hours, 2),
                    }
                )

    if not rows:
        st.success("No temporal leakage rows in dataset.")
        return

    leak_df = pd.DataFrame(rows)
    st.warning(f"{len(leak_df)} news row(s) would be excluded due to temporal leakage.")
    st.dataframe(leak_df, use_container_width=True)


def main() -> None:
    st.set_page_config(page_title="Faithful Evidence Forecasting", layout="wide")
    st.title("Faithful Evidence-Centric Financial News Forecasting")

    if not DATA_PATH.exists():
        st.error("Dataset not found. Run scripts/generate_sample_data.py first.")
        return

    groups = load_groups()

    if (OUTPUT_DIR / "prediction_results.csv").exists():
        pred_df, faith_df = load_output_tables()
    else:
        st.warning("Pipeline outputs not found. Run: python src/run_pipeline.py")
        pred_df, faith_df = pd.DataFrame(), pd.DataFrame()

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Prediction Overview", "Evidence Explorer", "Faithfulness Analysis", "Temporal Leakage"]
    )
    with tab1:
        render_prediction_overview(pred_df)
    with tab2:
        render_evidence_explorer(groups)
    with tab3:
        render_faithfulness(faith_df)
    with tab4:
        render_leakage_monitor(groups)


if __name__ == "__main__":
    main()
