"""Participant — My Workshops (Upcoming / Past)."""

from datetime import datetime

import streamlit as st

from styles import badge, empty_state
from mock_data import get_facilitator, get_workshop


def _registration_for(me, workshop_id):
    return next(
        (r for r in st.session_state.registrations
         if r["participant_id"] == me and r["workshop_id"] == workshop_id),
        None,
    )


def _upcoming_card(w, reg):
    fac = get_facilitator(w["facilitator_id"])
    st.markdown(
        f"""
        <div class="wiq-ws-card">
            <div>{badge(w['type'])} &nbsp; {badge(w['mode'])} &nbsp; {badge(reg['status'])}</div>
            <div class="wiq-ws-title">{w['title']}</div>
            <div class="wiq-ws-meta">📅 {w['date'].strftime('%a, %d %b')} · ⏰ {w['time'].strftime('%H:%M')}</div>
            <div class="wiq-ws-meta">👤 {fac['name']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    if c1.button("✅  Confirm Attendance", key=f"conf_{w['id']}", width="stretch"):
        reg["status"] = "Confirmed"
        st.toast("Attendance confirmed", icon="✅")
        st.rerun()
    if c2.button("❌  Can't Attend", key=f"dec_{w['id']}", width="stretch"):
        reg["status"] = "Declined"
        st.toast("Marked as can't attend", icon="📝")
        st.rerun()


def _past_card(w, reg):
    fac = get_facilitator(w["facilitator_id"])
    existing_fb = next(
        (f for f in st.session_state.feedback
         if f["workshop_id"] == w["id"]
         and f["participant_id"] == st.session_state.auth["participant_id"]),
        None,
    )

    st.markdown(
        f"""
        <div class="wiq-ws-card">
            <div>{badge(w['type'])} &nbsp; {badge('Completed')}</div>
            <div class="wiq-ws-title">{w['title']}</div>
            <div class="wiq-ws-meta">📅 {w['date'].strftime('%a, %d %b')} · 👤 {fac['name']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if existing_fb:
        st.success(f"You rated this {'★' * existing_fb['rating']} ({existing_fb['rating']}/5)")
    else:
        with st.expander("💬  Give Feedback"):
            rating = st.slider("Rating", 1, 5, 4, key=f"r_{w['id']}")
            comment = st.text_area(
                "What worked, what didn't?",
                key=f"c_{w['id']}",
                placeholder="A line or two is plenty.",
                height=100,
            )
            if st.button("Submit feedback", type="primary", key=f"submit_{w['id']}"):
                st.session_state.feedback.append({
                    "id":             f"fb-self-{w['id']}",
                    "workshop_id":    w["id"],
                    "participant_id": st.session_state.auth["participant_id"],
                    "rating":         int(rating),
                    "comment":        comment.strip() or "—",
                    "submitted_on":   datetime.now().date(),
                })
                st.toast("Thanks for the feedback! 🙏", icon="✨")
                st.rerun()


def render():
    st.markdown("### My Workshops")
    me = st.session_state.auth["participant_id"]

    my_regs = [r for r in st.session_state.registrations if r["participant_id"] == me]
    pairs = [(get_workshop(r["workshop_id"]), r) for r in my_regs]
    pairs = [(w, r) for w, r in pairs if w is not None]

    upcoming = sorted([(w, r) for w, r in pairs if not w["is_past"]],
                      key=lambda x: x[0]["date"])
    past = sorted([(w, r) for w, r in pairs if w["is_past"]],
                  key=lambda x: x[0]["date"], reverse=True)

    tab_up, tab_past = st.tabs([f"📅  Upcoming ({len(upcoming)})", f"📚  Past ({len(past)})"])

    with tab_up:
        if not upcoming:
            empty_state(
                "📭", "Nothing on your calendar yet",
                "Head to Browse Workshops to register for something this month.",
            )
        else:
            cols_per_row = 2
            for i in range(0, len(upcoming), cols_per_row):
                row = st.columns(cols_per_row)
                for j, (w, r) in enumerate(upcoming[i:i + cols_per_row]):
                    with row[j]:
                        _upcoming_card(w, r)

    with tab_past:
        if not past:
            empty_state(
                "📖", "No past workshops yet",
                "Once you've attended a session, you'll be able to leave feedback here.",
            )
        else:
            cols_per_row = 2
            for i in range(0, len(past), cols_per_row):
                row = st.columns(cols_per_row)
                for j, (w, r) in enumerate(past[i:i + cols_per_row]):
                    with row[j]:
                        _past_card(w, r)
