"""HR Admin — Analytics."""

from datetime import datetime, timedelta
from collections import Counter, defaultdict

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def _attendance_trend(workshops, registrations):
    """Compute monthly attendance % for the trailing 6 months."""
    today = datetime.now().date()
    months = []
    for i in range(5, -1, -1):
        anchor = (today.replace(day=1) - timedelta(days=i * 30)).replace(day=1)
        months.append(anchor)

    rows = []
    for m_start in months:
        # End of month = start of next month minus a day
        if m_start.month == 12:
            m_end = m_start.replace(year=m_start.year + 1, month=1)
        else:
            m_end = m_start.replace(month=m_start.month + 1)

        ws_in_month = [
            w for w in workshops
            if w["is_past"] and m_start <= w["date"] < m_end
        ]
        if not ws_in_month:
            rows.append({"Month": m_start.strftime("%b %y"), "Attendance %": None})
            continue
        pcts = []
        for w in ws_in_month:
            regs = [r for r in registrations if r["workshop_id"] == w["id"]]
            if not regs: continue
            pcts.append(
                sum(1 for r in regs if r["status"] == "Confirmed") / len(regs) * 100
            )
        rows.append({
            "Month":        m_start.strftime("%b %y"),
            "Attendance %": round(sum(pcts) / len(pcts), 1) if pcts else None,
        })
    return pd.DataFrame(rows)


def _type_popularity(workshops, registrations):
    by_type = defaultdict(int)
    for w in workshops:
        n = sum(1 for r in registrations if r["workshop_id"] == w["id"])
        by_type[w["type"]] += n
    return pd.DataFrame(
        {"Type": list(by_type.keys()), "Registrations": list(by_type.values())}
    )


def _heatmap_data():
    """
    Synthesize a plausible day-of-week × time-of-day attendance heatmap.
    Values are deterministic so the demo always looks the same.
    """
    days  = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    slots = ["09:00", "11:00", "13:00", "15:00", "17:00"]
    rng = np.random.default_rng(7)
    base = rng.integers(55, 80, size=(len(days), len(slots)))
    # Pump up Tue 15:00 to match the hardcoded insight below
    base[1][3] = 85
    base[2][1] = 82
    base[3][3] = 78
    return days, slots, base


def render():
    st.markdown("### Analytics")
    st.caption("Cross-workshop trends and timing insights")

    workshops     = st.session_state.workshops
    registrations = st.session_state.registrations

    # ---- Insight cards ----
    c1, c2, c3 = st.columns(3)
    insight_card = lambda col, icon, title, body: col.markdown(
        f"""
        <div class="wiq-ai-card" style="min-height: 130px;">
            <div style="font-size: 1.4rem;">{icon}</div>
            <div style="font-weight:600; color:#111827; margin-top:4px;">{title}</div>
            <div style="color:#4B5563; font-size:0.9rem; margin-top:6px;">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    insight_card(
        c1, "📈", "Tuesday 3 PM is the sweet spot",
        "Workshops in this slot show 85% attendance — 12 pts above average.",
    )
    insight_card(
        c2, "🎯", "Technical workshops fill fastest",
        "Median time-to-full is 4 days for Technical vs. 9 days for Soft Skills.",
    )
    insight_card(
        c3, "🛟", "Reminders move the needle",
        "Sessions with a 24-hour reminder see 17% fewer no-shows.",
    )

    st.write("")

    # ---- Trend + popularity ----
    left, right = st.columns([1.4, 1])
    with left:
        st.markdown("##### Attendance trend (last 6 months)")
        df = _attendance_trend(workshops, registrations)
        fig = px.line(
            df, x="Month", y="Attendance %",
            markers=True,
            color_discrete_sequence=["#5B5BD6"],
        )
        fig.update_traces(line=dict(width=3))
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=320, yaxis_range=[0, 100],
            plot_bgcolor="white", xaxis_title=None,
        )
        st.plotly_chart(fig, width="stretch")

    with right:
        st.markdown("##### Workshop type popularity")
        df = _type_popularity(workshops, registrations)
        fig = px.bar(
            df, x="Registrations", y="Type",
            orientation="h",
            text="Registrations",
            color_discrete_sequence=["#8B5CF6"],
        )
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=320, plot_bgcolor="white",
            xaxis_title=None, yaxis_title=None,
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, width="stretch")

    # ---- Heatmap ----
    st.markdown("##### Best day & time for attendance")
    st.caption("Average attendance %, weekday × time slot")
    days, slots, values = _heatmap_data()
    fig = go.Figure(data=go.Heatmap(
        z=values,
        x=slots, y=days,
        colorscale=[[0, "#EEF2FF"], [1, "#5B5BD6"]],
        colorbar=dict(title="%"),
        hovertemplate="%{y} %{x}: %{z}%<extra></extra>",
        text=values, texttemplate="%{text}%",
    ))
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        height=320, plot_bgcolor="white",
    )
    st.plotly_chart(fig, width="stretch")
