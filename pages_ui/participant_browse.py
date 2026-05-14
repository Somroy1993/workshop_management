"""Participant — Browse upcoming workshops."""

import streamlit as st

from styles import badge, empty_state
from mock_data import get_facilitator, registrations_for


def render():
    st.markdown("### Browse workshops")
    st.caption("Pick something to learn this month")

    # ---- Filter chips ----
    if "browse_filter" not in st.session_state:
        st.session_state.browse_filter = "All"

    chips = ["All", "Technical", "Soft Skills", "Leadership", "Wellness"]
    chip_cols = st.columns(len(chips))
    for i, c in enumerate(chips):
        with chip_cols[i]:
            is_active = st.session_state.browse_filter == c
            label = f"✓ {c}" if is_active else c
            if st.button(label, key=f"chip_{c}", width="stretch",
                         type="primary" if is_active else "secondary"):
                st.session_state.browse_filter = c
                st.rerun()

    st.write("")

    upcoming = [w for w in st.session_state.workshops if not w["is_past"]]
    if st.session_state.browse_filter != "All":
        upcoming = [w for w in upcoming if w["type"] == st.session_state.browse_filter]
    upcoming = sorted(upcoming, key=lambda w: w["date"])

    if not upcoming:
        empty_state(
            "🗓️", "No workshops in this category",
            "Try a different filter — new sessions are added every week.",
        )
        return

    me = st.session_state.auth["participant_id"]
    my_reg_ids = {r["workshop_id"] for r in st.session_state.registrations
                  if r["participant_id"] == me}

    # ---- Card grid (3 columns) ----
    cols_per_row = 3
    for i in range(0, len(upcoming), cols_per_row):
        row = st.columns(cols_per_row)
        for j, w in enumerate(upcoming[i:i + cols_per_row]):
            with row[j]:
                fac = get_facilitator(w["facilitator_id"])
                regs = registrations_for(w["id"])
                spots_left = max(0, w["capacity"] - len(regs))

                st.markdown(
                    f"""
                    <div class="wiq-ws-card">
                        <div>
                            {badge(w['type'])} &nbsp; {badge(w['mode'])}
                        </div>
                        <div class="wiq-ws-title">{w['title']}</div>
                        <div class="wiq-ws-meta">📅 {w['date'].strftime('%a, %d %b')} · ⏰ {w['time'].strftime('%H:%M')}</div>
                        <div class="wiq-ws-meta">👤 {fac['name']}</div>
                        <div class="wiq-ws-meta">👥 {spots_left} spots left of {w['capacity']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                already = w["id"] in my_reg_ids
                if already:
                    st.button("✓ Registered", key=f"reg_{w['id']}",
                              disabled=True, width="stretch")
                else:
                    if st.button("Register", key=f"reg_{w['id']}",
                                 type="primary", width="stretch"):
                        st.session_state.selected_workshop_id = w["id"]
                        st.session_state.current_page = "Register"
                        st.rerun()
