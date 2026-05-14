"""HR Admin — Create Workshop form."""

from datetime import datetime, timedelta, time

import streamlit as st


def render():
    st.markdown("### Create a new workshop")
    st.caption("Fill in the details below. You can edit them later.")

    facilitators = st.session_state.facilitators

    with st.form("create_workshop", clear_on_submit=False, border=True):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Title *", placeholder="e.g. Coaching Conversations for Managers")
            wdate = st.date_input(
                "Date *",
                value=datetime.now().date() + timedelta(days=14),
                min_value=datetime.now().date(),
            )
            duration = st.number_input("Duration (minutes) *", min_value=30, max_value=480, value=90, step=15)
            wtype = st.selectbox(
                "Workshop type *",
                ["Technical", "Soft Skills", "Leadership", "Wellness"],
            )

        with col2:
            facilitator_label = st.selectbox(
                "Facilitator *",
                [f"{f['name']} — {f['expertise']}" for f in facilitators],
            )
            wtime = st.time_input("Start time *", value=time(15, 0))
            capacity = st.number_input("Capacity *", min_value=5, max_value=500, value=40, step=5)
            mode = st.selectbox("Mode *", ["Virtual", "In-person", "Hybrid"])

        description = st.text_area(
            "Description *",
            placeholder="What will participants learn? What should they bring? Any pre-reading?",
            height=140,
        )

        st.markdown("&nbsp;")
        submitted = st.form_submit_button("🚀  Publish Workshop", type="primary", width="stretch")

    if submitted:
        if not title.strip() or not description.strip():
            st.error("Title and description are required.")
            return

        facilitator = facilitators[
            [f"{f['name']} — {f['expertise']}" for f in facilitators].index(facilitator_label)
        ]

        new_id = f"w{len(st.session_state.workshops) + 1:03d}"
        new_workshop = {
            "id":             new_id,
            "title":          title.strip(),
            "description":    description.strip(),
            "date":           wdate,
            "time":           wtime,
            "duration_min":   int(duration),
            "facilitator_id": facilitator["id"],
            "type":           wtype,
            "mode":           mode,
            "capacity":       int(capacity),
            "status":         "Upcoming",
            "is_past":        False,
            "brief_idx":      len(st.session_state.workshops) % 4,
            "summary_idx":    len(st.session_state.workshops) % 3,
        }
        st.session_state.workshops.append(new_workshop)

        st.toast(f"Published “{title}” ✨", icon="🎉")
        st.success("Workshop published. Redirecting to the workshops list…")
        st.session_state.current_page = "Workshops"
        st.rerun()
