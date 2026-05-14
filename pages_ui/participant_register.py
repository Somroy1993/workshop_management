"""Participant — Register for a workshop."""

from datetime import datetime
import time as time_mod

import streamlit as st

from styles import badge
from mock_data import get_workshop, get_facilitator, registrations_for


def render():
    wid = st.session_state.get("selected_workshop_id")
    w = get_workshop(wid)
    if not w:
        st.warning("No workshop selected.")
        if st.button("← Browse workshops"):
            st.session_state.current_page = "Browse Workshops"
            st.rerun()
        return

    if st.button("← Back to browse"):
        st.session_state.current_page = "Browse Workshops"
        st.session_state.selected_workshop_id = None
        st.rerun()

    fac = get_facilitator(w["facilitator_id"])
    regs = registrations_for(w["id"])
    spots_left = max(0, w["capacity"] - len(regs))

    st.markdown(f"### {w['title']}")
    st.caption(
        f"{w['date'].strftime('%a, %d %b %Y')} · {w['time'].strftime('%H:%M')} · "
        f"{w['duration_min']} min · {fac['name']}"
    )

    c1, c2, c3 = st.columns(3)
    c1.markdown(f"**Type** &nbsp; {badge(w['type'])}", unsafe_allow_html=True)
    c2.markdown(f"**Mode** &nbsp; {badge(w['mode'])}", unsafe_allow_html=True)
    c3.markdown(f"**Spots left** &nbsp; **{spots_left}** of {w['capacity']}")

    st.write("")
    st.markdown("##### About this workshop")
    st.write(w["description"])

    st.write("")
    with st.form("register_form", border=True):
        st.markdown("##### Tell us what you're hoping to get out of this")
        expectations = st.text_area(
            "What do you hope to learn from this workshop? *",
            placeholder=(
                "e.g. I'd like concrete language for giving difficult feedback "
                "to peers without making it feel hierarchical."
            ),
            height=120,
        )
        st.caption("Your facilitator uses these inputs to tailor the session.")

        submit = st.form_submit_button(
            "✅  Confirm Registration", type="primary", width="stretch"
        )

    if submit:
        if not expectations.strip():
            st.error("Please share what you're hoping to learn — it really helps the facilitator.")
            return

        new_reg = {
            "id":             f"r-{w['id']}-{st.session_state.auth['participant_id']}",
            "workshop_id":    w["id"],
            "participant_id": st.session_state.auth["participant_id"],
            "registered_on":  datetime.now().date(),
            "expectations":   expectations.strip(),
            "status":         "Confirmed",
        }
        # Avoid duplicate entries
        st.session_state.registrations = [
            r for r in st.session_state.registrations if r["id"] != new_reg["id"]
        ]
        st.session_state.registrations.append(new_reg)

        with st.spinner("Securing your seat…"):
            time_mod.sleep(1.2)

        st.balloons()
        st.success(f"You're in! 🎉  We'll send a calendar invite to your inbox.")
        st.toast("Added to My Workshops", icon="📌")

        cta_l, cta_r = st.columns(2)
        if cta_l.button("View My Workshops", type="primary", width="stretch"):
            st.session_state.current_page = "My Workshops"
            st.rerun()
        if cta_r.button("Browse more", width="stretch"):
            st.session_state.current_page = "Browse Workshops"
            st.rerun()
