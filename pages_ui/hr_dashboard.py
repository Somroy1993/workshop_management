"""HR Admin — Dashboard (home)."""

from datetime import datetime, timedelta
from collections import Counter

import pandas as pd
import plotly.express as px
import streamlit as st

from styles import kpi_card, badge
from mock_data import (
    get_facilitator, registrations_for, feedback_for,
)


def _avg_attendance_pct():
    past = [w for w in st.session_state.workshops if w["is_past"]]
    if not past:
        return 0
    pct_list = []
    for w in past:
        regs = registrations_for(w["id"])
        if not regs:
            continue
        confirmed = sum(1 for r in regs if r["status"] == "Confirmed")
        pct_list.append(confirmed / len(regs) * 100)
    return round(sum(pct_list) / len(pct_list)) if pct_list else 0


def _sentiment_distribution():
    """Bucket past feedback ratings into Positive/Neutral/Critical."""
    counts = Counter()
    for f in st.session_state.feedback:
        if f["rating"] >= 4:
            counts["Positive"] += 1
        elif f["rating"] == 3:
            counts["Neutral"] += 1
        else:
            counts["Critical"] += 1
    return counts


def render():
    st.markdown("### Dashboard")
    st.caption(f"Overview as of {datetime.now().strftime('%a, %d %b %Y')}")

    workshops = st.session_state.workshops
    upcoming = [w for w in workshops if not w["is_past"]]

    # ---- KPI row ----
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Total Workshops",     len(workshops), "+2 this quarter")
    with c2: kpi_card("Upcoming Workshops",  len(upcoming))
    with c3: kpi_card("Total Registrations", len(st.session_state.registrations), "+18% MoM")
    with c4: kpi_card("Avg Attendance",      f"{_avg_attendance_pct()}%", "↑ 4 pts")

    st.write("")

    # ---- Charts row ----
    left, right = st.columns([1.4, 1])
    with left:
        st.markdown("##### Registrations per workshop")
        st.caption("Last 6 workshops by date")
        last6 = sorted(workshops, key=lambda w: w["date"])[-6:]
        df = pd.DataFrame([
            {
                "Workshop":      w["title"],
                "Registrations": len(registrations_for(w["id"])),
                "Capacity":      w["capacity"],
            }
            for w in last6
        ])
        fig = px.bar(
            df, x="Workshop", y="Registrations",
            text="Registrations",
            color_discrete_sequence=["#5B5BD6"],
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=320,
            xaxis_title=None, yaxis_title=None,
            plot_bgcolor="white",
        )
        fig.update_xaxes(tickangle=-20)
        st.plotly_chart(fig, width="stretch")

    with right:
        st.markdown("##### Participant sentiment")
        st.caption("Across all past feedback")
        sent = _sentiment_distribution()
        if sum(sent.values()) == 0:
            st.info("No feedback yet.")
        else:
            df = pd.DataFrame(
                {"Sentiment": list(sent.keys()), "Count": list(sent.values())}
            )
            fig = px.pie(
                df, names="Sentiment", values="Count", hole=0.55,
                color="Sentiment",
                color_discrete_map={
                    "Positive": "#1F7A45",
                    "Neutral":  "#B45309",
                    "Critical": "#B91C1C",
                },
            )
            fig.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                height=320, showlegend=True,
            )
            st.plotly_chart(fig, width="stretch")

    # ---- Upcoming workshops table ----
    st.markdown("##### Upcoming workshops")
    if not upcoming:
        st.info("No upcoming workshops scheduled.")
        return

    rows = []
    for w in sorted(upcoming, key=lambda x: x["date"]):
        regs = registrations_for(w["id"])
        rows.append({
            "Workshop":      w["title"],
            "Date":          w["date"].strftime("%a, %d %b"),
            "Time":          w["time"].strftime("%H:%M"),
            "Facilitator":   get_facilitator(w["facilitator_id"])["name"],
            "Registrations": f"{len(regs)} / {w['capacity']}",
            "Status":        w["status"],
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, width="stretch", hide_index=True)
