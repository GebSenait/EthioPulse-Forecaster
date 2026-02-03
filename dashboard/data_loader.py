"""
Dashboard data loading utilities for EthioPulse-Forecaster.
Loads reference data, forecast tables, and event-impact data for the Streamlit app.
"""

import pandas as pd
from pathlib import Path
from typing import Tuple, Optional

# Paths relative to project root (parent of dashboard/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"


def load_reference_data() -> pd.DataFrame:
    """Load unified reference data (observations, events, impact_links)."""
    path = DATA_DIR / "reference" / "task34_reference_data.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    return df


def load_observations(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Extract access and usage observation time series from unified data."""
    obs = df[df["record_type"] == "observation"].copy()
    if obs.empty:
        return pd.DataFrame(), pd.DataFrame()
    obs["year"] = pd.to_numeric(obs["year"], errors="coerce")
    obs = obs.dropna(subset=["year", "value"])
    access = obs[obs["pillar"] == "access"].groupby("year")["value"].mean().sort_index()
    usage = obs[obs["pillar"] == "usage"].groupby("year")["value"].mean().sort_index()
    access_df = access.reset_index()
    access_df.columns = ["year", "value"]
    access_df["pillar"] = "Access (Account Ownership)"
    usage_df = usage.reset_index()
    usage_df.columns = ["year", "value"]
    usage_df["pillar"] = "Usage (Digital Payments)"
    return access_df, usage_df


def load_events(df: pd.DataFrame) -> pd.DataFrame:
    """Extract events with year and event_name."""
    events = df[df["record_type"] == "event"].copy()
    if events.empty:
        return pd.DataFrame()
    events["year"] = pd.to_numeric(events["year"], errors="coerce")
    # event_name may be in event_name or a similar column
    name_col = "event_name" if "event_name" in events.columns else "source_event"
    if name_col not in events.columns and "event_type" in events.columns:
        events["event_name"] = events.get("event_type", "")
    elif name_col in events.columns:
        events["event_name"] = events[name_col].fillna(events.get("event_type", ""))
    return events[["year", "event_name", "event_type"]].dropna(subset=["year"])


def load_impact_links(df: pd.DataFrame) -> pd.DataFrame:
    """Extract impact_link records and join to event names where possible."""
    links = df[df["record_type"] == "impact_link"].copy()
    if links.empty:
        return pd.DataFrame()
    events = df[df["record_type"] == "event"].copy()
    events = events.rename(columns={"record_id": "source_event"})
    # record_id in CSV is row number; source_event references event record_id
    id_col = "record_id" if "record_id" in df.columns else None
    if id_col and "source_event" in links.columns and "event_name" in events.columns:
        event_lookup = events.set_index("source_event")[["event_name", "year"]].to_dict("index")
        links["event_name"] = links["source_event"].map(
            lambda x: event_lookup.get(x, {}).get("event_name", f"Event {x}")
        )
        links["event_year"] = links["source_event"].map(
            lambda x: event_lookup.get(x, {}).get("year", None)
        )
    return links


def load_forecast_baseline() -> pd.DataFrame:
    """Load baseline forecast table with confidence intervals."""
    path = REPORTS_DIR / "task4_forecast_table_2025_2027.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def load_forecast_scenarios() -> pd.DataFrame:
    """Load scenario-based forecasts (baseline, optimistic, pessimistic)."""
    path = REPORTS_DIR / "task4_forecast_scenarios.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def get_events_with_impacts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build event-impact summary: event name, year, and which indicators they affect.
    Uses impact_link source_event -> event, target_observation -> observation pillar.
    """
    obs = df[df["record_type"] == "observation"].copy()
    events = df[df["record_type"] == "event"].copy()
    links = df[df["record_type"] == "impact_link"].copy()
    if obs.empty or events.empty or links.empty:
        return pd.DataFrame()
    # CSV has record_id as first column (1-based row index)
    if "record_id" not in df.columns and len(df.columns) > 0:
        obs["_rid"] = obs.index + 1
        events["_rid"] = events.index + 1
    else:
        obs["_rid"] = obs["record_id"]
        events["_rid"] = events["record_id"]
    id_to_pillar = obs.set_index("_rid")["pillar"].to_dict()
    event_id_to_name = events.set_index("_rid")["event_name"].to_dict() if "event_name" in events.columns else {}
    event_id_to_year = events.set_index("_rid")["year"].to_dict()
    rows = []
    for _, row in links.iterrows():
        se = row.get("source_event")
        to = row.get("target_observation")
        if pd.isna(se) or pd.isna(to):
            continue
        try:
            se, to = int(float(se)), int(float(to))
        except (ValueError, TypeError):
            continue
        indicator = id_to_pillar.get(to, "Unknown")
        name = event_id_to_name.get(se)
        if name is None or (isinstance(name, float) and pd.isna(name)):
            match = events[events["_rid"] == se]
            if len(match) > 0 and "event_type" in match.columns:
                name = match["event_type"].iloc[0]
            else:
                name = f"Event {se}"
        rows.append({
            "event_name": name,
            "event_year": event_id_to_year.get(se),
            "indicator": indicator,
            "direction": row.get("impact_direction", "positive"),
            "magnitude": row.get("impact_magnitude"),
            "lag_months": row.get("lag_months"),
        })
    if not rows:
        return pd.DataFrame()
    out = pd.DataFrame(rows)
    out["event_year"] = pd.to_numeric(out["event_year"], errors="coerce")
    return out
