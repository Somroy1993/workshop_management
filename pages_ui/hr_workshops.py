"""HR Admin — Workshops list view (table)."""

import pandas as pd
import streamlit as st

from styles import badge
from mock_data import get_facilitator, registrations_for


def render():
    top_l, top_r = st.columns([3, 1])
    with top_l:
        st.markdown("### Workshops")
        st.caption("All workshops across past, ongoing, and upcoming")
    with top_r:
        st.write("")
        if st.button("＋ Create New Workshop", type="primary", width="stretch"):
            st.session_state.current_page = "Create Workshop"
            st.rerun()

    workshops = sorted(st.session_state.workshops, key=lambda w: w["date"], reverse=True)

    # ----- Filters -----
    f1, f2, f3 = st.columns([1, 1, 2])
    with f1:
        type_filter = st.selectbox(
            "Type", ["All", "Technical", "Soft Skills", "Leadership", "Wellness"]
        )
    with f2:
        status_filter = st.selectbox(
            "Status", ["All", "Upcoming", "Starting Soon", "Completed"]
        )
    with f3:
        search = st.text_input("Search by title", placeholder="e.g. feedback, Kubernetes")

    filtered = [
        w for w in workshops
        if (type_filter   == "All" or w["type"]   == type_filter)
        and (status_filter == "All" or w["status"] == status_filter)
        and (not search or search.lower() in w["title"].lower())
    ]

    if not filtered:
        st.info("No workshops match your filters.")
        return

    # ----- Table -----
    rows = []
    for w in filtered:
        regs = registrations_for(w["id"])
        rows.append({
            "Title":         w["title"],
            "Date":          w["date"].strftime("%a, %d %b %Y"),
            "Facilitator":   get_facilitator(w["facilitator_id"])["name"],
            "Type":          w["type"],
            "Mode":          w["mode"],
            "Registrations": f"{len(regs)} / {w['capacity']}",
            "Status":        w["status"],
            "_id":           w["id"],
        })
    df = pd.DataFrame(rows)

    # st.dataframe is fast but doesn't let us put HTML badges in cells.
    # Render as a real table + a row of "Open" buttons below for navigation.
    st.dataframe(
        df.drop(columns=["_id"]),
        width="stretch",
        hide_index=True,
    )

    st.write("")
    st.markdown("##### Open a workshop")
    cols = st.columns(min(4, len(filtered)))
    for i, w in enumerate(filtered[:12]):
        with cols[i % len(cols)]:
            if st.button(
                f"📂  {w['title']}",
                key=f"open_{w['id']}",
                width="stretch",
            ):
                st.session_state.selected_workshop_id = w["id"]
                st.session_state.current_page = "Workshop Details"
                st.rerun()
