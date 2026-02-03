"""
EthioPulse-Forecaster — Interactive Dashboard (Task 5)

Stakeholder-ready dashboard for Ethiopia's financial inclusion indicators,
event impacts, and forecasts. Built with Streamlit for policy and investment decisions.

Sections: Overview | Trends | Forecasts | Inclusion Projections
"""

import sys
from pathlib import Path

# Ensure project root and dashboard dir are on path for imports
_DASHBOARD_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _DASHBOARD_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
if str(_DASHBOARD_DIR) not in sys.path:
    sys.path.insert(0, str(_DASHBOARD_DIR))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data_loader import (
    load_reference_data,
    load_observations,
    load_events,
    load_forecast_baseline,
    load_forecast_scenarios,
    get_events_with_impacts,
)

# Page config
st.set_page_config(
    page_title="EthioPulse-Forecaster | Financial Inclusion Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for stakeholder-ready UX
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #2E86AB 100%);
        color: white;
        padding: 1rem 1.25rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .metric-card h3 { margin: 0; font-size: 1.75rem; }
    .metric-card p { margin: 0.25rem 0 0 0; opacity: 0.9; font-size: 0.9rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { padding: 12px 20px; border-radius: 8px; }
    div[data-testid="stExpander"] { border: 1px solid #2E86AB; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# Load data once
@st.cache_data
def load_all():
    df = load_reference_data()
    access_df, usage_df = load_observations(df)
    events_df = load_events(df)
    impact_summary = get_events_with_impacts(df)
    forecast_baseline = load_forecast_baseline()
    forecast_scenarios = load_forecast_scenarios()
    return df, access_df, usage_df, events_df, impact_summary, forecast_baseline, forecast_scenarios

df, access_df, usage_df, events_df, impact_summary, forecast_baseline, forecast_scenarios = load_all()
data_loaded = not df.empty and (not access_df.empty or not usage_df.empty)

# Sidebar
st.sidebar.title("📊 EthioPulse-Forecaster")
st.sidebar.markdown("**Ethiopia Financial Inclusion Analytics**")
st.sidebar.markdown("---")
st.sidebar.caption("Selam Analytics · NBE & Development Finance Consortium")
if not data_loaded:
    st.sidebar.warning("Reference data not found. Using demo/empty views.")

# Navigation
page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Trends", "Forecasts", "Inclusion Projections"],
    index=0,
)

# ---------- OVERVIEW PAGE ----------
if page == "Overview":
    st.title("Overview — Key Metrics")
    st.markdown("Current values, trends, and the **Usage-to-Access Ratio** (digital activation indicator).")

    if data_loaded:
        # Latest values
        access_latest = access_df["value"].iloc[-1] if not access_df.empty else None
        usage_latest = usage_df["value"].iloc[-1] if not usage_df.empty else None
        year_latest = int(access_df["year"].iloc[-1]) if not access_df.empty else (int(usage_df["year"].iloc[-1]) if not usage_df.empty else None)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Account ownership (Access) %", f"{access_latest:.1f}" if access_latest is not None else "—", f"Latest: {year_latest}")
        with col2:
            st.metric("Digital payments (Usage) %", f"{usage_latest:.1f}" if usage_latest is not None else "—", f"Latest: {year_latest}")
        with col3:
            # P2P/ATM Crossover Ratio = Usage/Access (digital activation ratio)
            if access_latest and access_latest > 0 and usage_latest is not None:
                ratio = usage_latest / access_latest
                st.metric("Usage-to-Access Ratio", f"{ratio:.2f}", "Digital activation (higher = more usage per account)")
            else:
                st.metric("Usage-to-Access Ratio", "—", "Digital activation")
        with col4:
            if access_latest and usage_latest is not None and access_latest > 0:
                gap = access_latest - usage_latest
                st.metric("Access–Usage gap (pp)", f"{gap:.1f}", "Lower is better")

        # Growth rate highlights
        st.subheader("Growth rate highlights")
        if len(access_df) >= 2 and len(usage_df) >= 2:
            access_growth = (access_df["value"].iloc[-1] - access_df["value"].iloc[0]) / max(access_df["value"].iloc[0], 1e-6) * 100
            usage_growth = (usage_df["value"].iloc[-1] - usage_df["value"].iloc[0]) / max(usage_df["value"].iloc[0], 1e-6) * 100
            c1, c2 = st.columns(2)
            with c1:
                st.info(f"**Access** (full period): {access_growth:.1f}% growth")
            with c2:
                st.info(f"**Usage** (full period): {usage_growth:.1f}% growth")

        # Usage-to-Access ratio over time (indicator)
        st.subheader("Usage-to-Access Ratio over time")
        if not access_df.empty and not usage_df.empty:
            merge_df = access_df.rename(columns={"value": "access"}).merge(
                usage_df.rename(columns={"value": "usage"}),
                on="year",
                how="outer"
            ).sort_values("year")
            merge_df["ratio"] = merge_df["usage"] / merge_df["access"].replace(0, 1e-6)
            fig_ratio = go.Figure()
            fig_ratio.add_trace(go.Scatter(
                x=merge_df["year"], y=merge_df["ratio"],
                mode="lines+markers", name="Usage / Access",
                line=dict(color="#2E86AB", width=2), marker=dict(size=10)
            ))
            fig_ratio.add_hline(y=1.0, line_dash="dash", line_color="gray", annotation_text="Ratio = 1")
            fig_ratio.update_layout(
                title="Digital Activation Ratio (Usage ÷ Access)",
                xaxis_title="Year",
                yaxis_title="Ratio",
                template="plotly_white",
                height=400,
            )
            st.plotly_chart(fig_ratio, use_container_width=True)
            st.caption("When the ratio approaches 1, digital payment usage is catching up to account ownership.")

        # Event-impact summary (which events most affected indicators)
        if not impact_summary.empty:
            st.subheader("Events with measured impact on indicators")
            impact_agg = impact_summary.groupby("event_name").agg(
                magnitude=("magnitude", "sum"),
                indicators=("indicator", lambda x: ", ".join(sorted(set(x)))),
            ).reset_index()
            impact_agg = impact_agg.sort_values("magnitude", ascending=True)
            fig_impact = px.bar(
                impact_agg,
                x="magnitude",
                y="event_name",
                orientation="h",
                title="Cumulative impact magnitude by event (Task 3 impact links)",
                labels={"magnitude": "Impact magnitude", "event_name": "Event"},
            )
            fig_impact.update_layout(template="plotly_white", height=max(300, len(impact_agg) * 35))
            st.plotly_chart(fig_impact, use_container_width=True)
    else:
        st.info("Run Task 1 (or use reference data) to populate Overview metrics.")

# ---------- TRENDS PAGE ----------
elif page == "Trends":
    st.title("Trends — Time series & channel comparison")
    st.markdown("Explore historical **Access** (account ownership) and **Usage** (digital payments) with date range and channel comparison.")

    if data_loaded:
        combined = pd.concat([access_df, usage_df], ignore_index=True)
        if combined.empty:
            st.warning("No observation data available.")
        else:
            y_min = int(combined["year"].min())
            y_max = int(combined["year"].max())
            y_range = st.slider("Select year range", min_value=y_min, max_value=y_max, value=(y_min, y_max))
            filtered = combined[(combined["year"] >= y_range[0]) & (combined["year"] <= y_range[1])]

            fig_trend = px.line(
                filtered,
                x="year",
                y="value",
                color="pillar",
                markers=True,
                title="Access vs Usage over time",
                labels={"value": "Rate (%)", "year": "Year", "pillar": "Indicator"},
            )
            fig_trend.update_layout(
                template="plotly_white",
                height=500,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            fig_trend.for_each_trace(lambda t: t.update(line=dict(width=3)))
            st.plotly_chart(fig_trend, use_container_width=True)

            # Channel comparison: bar by year
            st.subheader("Channel comparison by year")
            pivot = filtered.pivot_table(index="year", columns="pillar", values="value").reset_index()
            if not pivot.empty:
                fig_bar = go.Figure()
                for col in pivot.columns:
                    if col == "year":
                        continue
                    fig_bar.add_trace(go.Bar(name=col, x=pivot["year"], y=pivot[col]))
                fig_bar.update_layout(barmode="group", title="Access vs Usage by year", template="plotly_white", height=400)
                st.plotly_chart(fig_bar, use_container_width=True)

            # Events overlay
            if not events_df.empty:
                st.subheader("Events timeline")
                events_filtered = events_df[(events_df["year"] >= y_range[0]) & (events_df["year"] <= y_range[1])]
                st.dataframe(events_filtered, use_container_width=True, hide_index=True)
    else:
        st.info("Load reference data to view trends.")

# ---------- FORECASTS PAGE ----------
elif page == "Forecasts":
    st.title("Forecasts — 2025–2027")
    st.markdown("Forecast visualizations with confidence intervals and **scenario selection** (baseline / event-augmented / optimistic / pessimistic).")

    if not forecast_baseline.empty or not forecast_scenarios.empty:
        model_option = st.selectbox(
            "Model / scenario view",
            ["Baseline with confidence intervals", "Scenario comparison (baseline / optimistic / pessimistic)"],
            index=0,
        )

        if model_option == "Baseline with confidence intervals" and not forecast_baseline.empty:
            fig_fc = go.Figure()
            for ind in forecast_baseline["Indicator"].unique():
                sub = forecast_baseline[forecast_baseline["Indicator"] == ind]
                fig_fc.add_trace(go.Scatter(
                    x=sub["Year"], y=sub["Baseline"],
                    mode="lines+markers", name=f"{ind} (baseline)",
                    line=dict(width=3),
                ))
                fig_fc.add_trace(go.Scatter(
                    x=sub["Year"], y=sub["High_CI"],
                    mode="lines", name=f"{ind} (upper CI)",
                    line=dict(width=1, dash="dash"),
                ))
                fig_fc.add_trace(go.Scatter(
                    x=sub["Year"], y=sub["Low_CI"],
                    mode="lines", name=f"{ind} (lower CI)",
                    line=dict(width=1, dash="dash"),
                ))
            fig_fc.update_layout(
                title="Forecast 2025–2027 (Baseline & confidence intervals)",
                xaxis_title="Year",
                yaxis_title="Rate (%)",
                template="plotly_white",
                height=500,
            )
            st.plotly_chart(fig_fc, use_container_width=True)

            st.subheader("Key projected milestones (baseline)")
            st.dataframe(forecast_baseline, use_container_width=True, hide_index=True)

        elif model_option == "Scenario comparison (baseline / optimistic / pessimistic)" and not forecast_scenarios.empty:
            scenario_sel = st.multiselect(
                "Scenarios to display",
                ["baseline", "optimistic", "pessimistic"],
                default=["baseline", "optimistic", "pessimistic"],
            )
            if scenario_sel:
                sub = forecast_scenarios[forecast_scenarios["Scenario"].isin(scenario_sel)]
                fig_sc = px.line(
                    sub,
                    x="Year",
                    y="Value",
                    color="Scenario",
                    facet_row="Indicator",
                    markers=True,
                    title="Forecast by scenario",
                    labels={"Value": "Rate (%)"},
                )
                fig_sc.update_layout(template="plotly_white", height=500)
                st.plotly_chart(fig_sc, use_container_width=True)
            st.subheader("Scenario table")
            st.dataframe(forecast_scenarios, use_container_width=True, hide_index=True)
    else:
        st.warning("No forecast data found. Run Task 4 and ensure `task4_forecast_table_2025_2027.csv` and `task4_forecast_scenarios.csv` exist in `reports/`.")

# ---------- INCLUSION PROJECTIONS PAGE ----------
elif page == "Inclusion Projections":
    st.title("Inclusion Projections — Progress toward 60% target")
    st.markdown("Financial inclusion rate projections and progress toward the **60% account ownership target** with scenario selector.")

    TARGET_PCT = 60.0
    st.subheader(f"Target: {TARGET_PCT}% account ownership (Access)")

    if not forecast_scenarios.empty:
        scenario_choice = st.radio("Scenario", ["optimistic", "baseline", "pessimistic"], index=1, horizontal=True)
        access_sc = forecast_scenarios[(forecast_scenarios["Indicator"] == "Access") & (forecast_scenarios["Scenario"] == scenario_choice)]
        if not access_sc.empty:
            fig_target = go.Figure()
            fig_target.add_trace(go.Scatter(
                x=access_sc["Year"], y=access_sc["Value"],
                mode="lines+markers", name=f"Access ({scenario_choice})",
                line=dict(width=3),
            ))
            fig_target.add_hline(y=TARGET_PCT, line_dash="dash", line_color="green", annotation_text=f"Target {TARGET_PCT}%")
            # Add historical if available
            if data_loaded and not access_df.empty:
                fig_target.add_trace(go.Scatter(
                    x=access_df["year"], y=access_df["value"],
                    mode="lines+markers", name="Historical Access",
                    line=dict(color="gray", width=2, dash="dot"),
                ))
            fig_target.update_layout(
                title="Access (Account Ownership) — Progress toward 60% target",
                xaxis_title="Year",
                yaxis_title="Rate (%)",
                template="plotly_white",
                height=450,
            )
            st.plotly_chart(fig_target, use_container_width=True)

            latest_proj = access_sc["Value"].iloc[-1]
            st.metric("Projected Access (2027)", f"{latest_proj:.1f}%", f"Target: {TARGET_PCT}% — {'On track' if latest_proj >= TARGET_PCT else 'Gap: ' + str(round(TARGET_PCT - latest_proj, 1)) + ' pp'}")

        st.subheader("Answers to consortium questions")
        with st.expander("Which events most affected financial inclusion indicators?"):
            if not impact_summary.empty:
                st.dataframe(impact_summary, use_container_width=True, hide_index=True)
            else:
                st.write("Event-impact links are derived from Task 3. Run Task 3 and ensure reference data includes impact_link records.")
        with st.expander("How did account ownership and digital payment usage evolve over time?"):
            st.write("See the **Trends** page for time series. Access grew from ~14% (2011) to ~54% (2024); Usage from ~2% to ~33%, with a persistent access–usage gap.")
        with st.expander("What is the forecast for Access and Usage through 2027?"):
            st.write("See the **Forecasts** page. Baseline 2027: Access ~82%, Usage ~52%. Optimistic and pessimistic scenarios bracket policy and market uncertainty.")
        with st.expander("What progress has Ethiopia made toward financial inclusion targets?"):
            st.write("Access is projected to exceed the 60% target under baseline and optimistic scenarios by 2027. Usage continues to lag; activation and interoperability remain levers.")
    else:
        st.info("Load scenario forecast data (Task 4) to view inclusion projections.")

# ---------- DATA DOWNLOAD (sidebar) ----------
st.sidebar.markdown("---")
st.sidebar.subheader("Data download")
if data_loaded:
    combined_obs = pd.concat([access_df, usage_df], ignore_index=True) if not access_df.empty or not usage_df.empty else pd.DataFrame()
    if not combined_obs.empty:
        st.sidebar.download_button(
            "Download observations (CSV)",
            combined_obs.to_csv(index=False).encode("utf-8"),
            file_name="ethiopia_fi_observations.csv",
            mime="text/csv",
        )
if not forecast_baseline.empty:
    st.sidebar.download_button(
        "Download baseline forecast (CSV)",
        forecast_baseline.to_csv(index=False).encode("utf-8"),
        file_name="task4_forecast_baseline.csv",
        mime="text/csv",
        key="dl_baseline",
    )
if not forecast_scenarios.empty:
    st.sidebar.download_button(
        "Download scenario forecast (CSV)",
        forecast_scenarios.to_csv(index=False).encode("utf-8"),
        file_name="task4_forecast_scenarios.csv",
        mime="text/csv",
        key="dl_scenarios",
    )

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Task 5 · EthioPulse-Forecaster · Reproducible & policy-ready")
