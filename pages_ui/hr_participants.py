"""HR Admin — Participants (people management)."""

import pandas as pd
import streamlit as st


def _stats_for_participant(pid):
    regs = [r for r in st.session_state.registrations if r["participant_id"] == pid]
    past_regs = []
    for r in regs:
        w = next((x for x in st.session_state.workshops if x["id"] == r["workshop_id"]), None)
        if w and w["is_past"]:
            past_regs.append(r)
    attended = sum(1 for r in past_regs if r["status"] == "Confirmed")
    no_shows = sum(1 for r in past_regs if r["status"] == "No-show")
    return attended, no_shows


def render():
    st.markdown("### Participants")
    st.caption("Everyone in your workshop ecosystem")

    participants = st.session_state.participants
    departments = sorted({p["department"] for p in participants})

    c1, c2 = st.columns([1, 3])
    with c1:
        dept_filter = st.selectbox("Department", ["All"] + departments)
    with c2:
        search = st.text_input("Search by name or email", placeholder="e.g. Priya")

    filtered = [
        p for p in participants
        if (dept_filter == "All" or p["department"] == dept_filter)
        and (
            not search
            or search.lower() in p["name"].lower()
            or search.lower() in p["email"].lower()
        )
    ]

    rows = []
    for p in filtered:
        attended, no_shows = _stats_for_participant(p["id"])
        flag = "🚩 Frequent drop-off" if no_shows > 2 else ""
        rows.append({
            "Name":       p["name"],
            "Email":      p["email"],
            "Department": p["department"],
            "Attended":   attended,
            "No-shows":   no_shows,
            "Flag":       flag,
        })
    df = pd.DataFrame(rows)

    # Quick summary banner
    flagged = sum(1 for r in rows if r["Flag"])
    if flagged:
        st.warning(
            f"⚠️  {flagged} participant(s) have more than 2 no-shows. "
            "Consider a follow-up nudge or check-in."
        )

    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
        column_config={
            "Attended": st.column_config.NumberColumn(format="%d"),
            "No-shows": st.column_config.NumberColumn(format="%d"),
        },
    )
