"""HR Admin — Workshop Details (drill-down)."""

import time as time_mod

import pandas as pd
import plotly.express as px
import streamlit as st

from styles import badge
from mock_data import (
    get_workshop, get_facilitator, get_participant,
    registrations_for, feedback_for,
    brief_for_workshop, summary_for_workshop,
)


def _render_header(w):
    fac = get_facilitator(w["facilitator_id"])
    regs = registrations_for(w["id"])
    seats_filled = len(regs)

    if st.button("← Back to workshops"):
        st.session_state.current_page = "Workshops"
        st.session_state.selected_workshop_id = None
        st.rerun()

    st.markdown(f"### {w['title']}")
    meta = " · ".join([
        w["date"].strftime("%a, %d %b %Y"),
        w["time"].strftime("%H:%M"),
        f"{w['duration_min']} min",
        fac["name"],
    ])
    st.caption(meta)

    cols = st.columns([1, 1, 1, 1])
    cols[0].markdown(f"**Type** &nbsp; {badge(w['type'])}", unsafe_allow_html=True)
    cols[1].markdown(f"**Mode** &nbsp; {badge(w['mode'])}", unsafe_allow_html=True)
    cols[2].markdown(f"**Status** &nbsp; {badge(w['status'])}", unsafe_allow_html=True)
    cols[3].markdown(f"**Seats** &nbsp; **{seats_filled} / {w['capacity']}**")

    with st.expander("Description"):
        st.write(w["description"])


def _render_registrations_tab(w):
    regs = registrations_for(w["id"])
    if not regs:
        st.info("No registrations yet.")
        return

    confirmed_capacity_cap = w["capacity"]
    confirmed_or_pending = [r for r in regs if r["status"] in ("Confirmed", "Pending")]
    main = confirmed_or_pending[:confirmed_capacity_cap]
    waitlist = confirmed_or_pending[confirmed_capacity_cap:]
    other = [r for r in regs if r["status"] not in ("Confirmed", "Pending")]

    def row(r):
        p = get_participant(r["participant_id"])
        return {
            "Name":         p["name"],
            "Email":        p["email"],
            "Department":   p["department"],
            "Registered":   r["registered_on"].strftime("%d %b"),
            "Expectations": r["expectations"] or "—",
            "Status":       r["status"],
        }

    st.markdown("##### Registered participants")
    df_main = pd.DataFrame([row(r) for r in main + other])
    st.dataframe(df_main, width="stretch", hide_index=True)

    if waitlist:
        st.markdown("##### Waitlist")
        st.caption(f"{len(waitlist)} participant(s) waiting for a seat")
        df_wait = pd.DataFrame([row(r) for r in waitlist])
        st.dataframe(df_wait, width="stretch", hide_index=True)


def _render_brief_card(brief):
    items_themes = "".join(f"<li>{t}</li>" for t in brief["top_themes"])
    items_concerns = "".join(f"<li>{c}</li>" for c in brief["key_concerns"])
    items_points = "".join(f"<li>{p}</li>" for p in brief["talking_points"])

    st.markdown(
        f"""
        <div class="wiq-ai-card">
            <span class="wiq-ai-pill">AI BRIEF</span>
            <div class="wiq-ai-section-title">Top themes</div>
            <ul>{items_themes}</ul>
            <div class="wiq-ai-section-title">Sentiment summary</div>
            <div>{brief['sentiment_summary']}</div>
            <div class="wiq-ai-section-title">Key concerns</div>
            <ul>{items_concerns}</ul>
            <div class="wiq-ai-section-title">Recommended talking points</div>
            <ul>{items_points}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_brief_tab(w):
    regs = registrations_for(w["id"])
    sample_size = sum(1 for r in regs if r["expectations"])

    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown(
            f"Synthesized from **{sample_size}** participant expectations submitted at registration."
        )
    with c2:
        if st.button("🔄  Regenerate Brief", width="stretch"):
            with st.spinner("Re-analyzing participant inputs…"):
                time_mod.sleep(2)
            st.toast("Brief regenerated", icon="✨")

    _render_brief_card(brief_for_workshop(w["id"]))


def _render_feedback_tab(w):
    if not w["is_past"]:
        st.info("Feedback will appear here after the workshop is completed.")
        return

    fb = feedback_for(w["id"])
    if not fb:
        st.info("No feedback collected yet.")
        return

    avg = sum(f["rating"] for f in fb) / len(fb)
    stars = "★" * round(avg) + "☆" * (5 - round(avg))

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("##### Overall rating")
        st.markdown(
            f"<div style='font-size:2rem; color:#F59E0B; letter-spacing:4px;'>{stars}</div>"
            f"<div style='color:#6B7280;'>{avg:.1f} / 5 · {len(fb)} responses</div>",
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown("##### Rating distribution")
        dist = {i: 0 for i in range(1, 6)}
        for f in fb:
            dist[f["rating"]] += 1
        df = pd.DataFrame(
            {"Rating": [f"{r}★" for r in dist.keys()], "Count": list(dist.values())}
        )
        fig = px.bar(
            df, x="Rating", y="Count", text="Count",
            color_discrete_sequence=["#5B5BD6"],
        )
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=220, xaxis_title=None, yaxis_title=None,
            plot_bgcolor="white", showlegend=False,
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, width="stretch")

    # ----- AI summary card -----
    s = summary_for_workshop(w["id"])
    pos = "".join(f"<li>{x}</li>" for x in s["top_positives"])
    imp = "".join(f"<li>{x}</li>" for x in s["top_improvements"])
    act = "".join(f"<li>{x}</li>" for x in s["action_items"])
    st.markdown(
        f"""
        <div class="wiq-ai-card">
            <span class="wiq-ai-pill">AI SUMMARY</span>
            <div class="wiq-ai-section-title">Top positives</div>
            <ul>{pos}</ul>
            <div class="wiq-ai-section-title">Top improvements</div>
            <ul>{imp}</ul>
            <div class="wiq-ai-section-title">Suggested action items</div>
            <ul>{act}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ----- Raw comments -----
    st.markdown("##### Individual feedback")
    rows = []
    for f in fb:
        p = get_participant(f["participant_id"])
        rows.append({
            "Participant": p["name"],
            "Rating":      "★" * f["rating"],
            "Comment":     f["comment"],
            "Submitted":   f["submitted_on"].strftime("%d %b"),
        })
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)


def render():
    wid = st.session_state.get("selected_workshop_id")
    w = get_workshop(wid) if wid else None
    if not w:
        st.warning("No workshop selected.")
        if st.button("← Back to workshops"):
            st.session_state.current_page = "Workshops"
            st.rerun()
        return

    _render_header(w)

    tab1, tab2, tab3 = st.tabs(["📋  Registrations", "🤖  Facilitator Brief", "💬  Feedback & Insights"])
    with tab1: _render_registrations_tab(w)
    with tab2: _render_brief_tab(w)
    with tab3: _render_feedback_tab(w)
