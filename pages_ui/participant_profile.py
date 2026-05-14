"""Participant — Profile (placeholder)."""

import streamlit as st

from mock_data import get_participant


def render():
    me_id = st.session_state.auth["participant_id"]
    me = get_participant(me_id)
    if not me:
        st.warning("Profile unavailable in demo mode.")
        return

    my_regs = [r for r in st.session_state.registrations if r["participant_id"] == me_id]
    workshops_by_id = {w["id"]: w for w in st.session_state.workshops}
    attended_count = sum(
        1 for r in my_regs
        if workshops_by_id.get(r["workshop_id"], {}).get("is_past")
        and r["status"] == "Confirmed"
    )
    fb_given = sum(
        1 for f in st.session_state.feedback if f["participant_id"] == me_id
    )

    # --- Profile header card ---
    initials = "".join([part[0] for part in me["name"].split()[:2]]).upper()
    st.markdown(
        f"""
        <div class="wiq-card" style="display:flex; gap:18px; align-items:center;">
          <div style="
              width:64px; height:64px; border-radius:50%;
              background: linear-gradient(135deg, #5B5BD6 0%, #8B5CF6 100%);
              color:#fff; display:flex; align-items:center; justify-content:center;
              font-weight:700; font-size:22px;">
            {initials}
          </div>
          <div>
              <div style="font-size:1.2rem; font-weight:700;">{me['name']}</div>
              <div style="color:#6B7280;">{me['email']} · {me['department']}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- Stat tiles ---
    c1, c2, c3 = st.columns(3)
    for col, label, value in [
        (c1, "Workshops attended", attended_count),
        (c2, "Currently registered", sum(1 for r in my_regs if not workshops_by_id.get(r["workshop_id"], {}).get("is_past"))),
        (c3, "Feedback given", fb_given),
    ]:
        with col:
            st.markdown(
                f"""
                <div class="wiq-kpi">
                    <div class="wiq-kpi-label">{label}</div>
                    <div class="wiq-kpi-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    # --- Badges (gamified, mock) ---
    st.markdown("##### Your badges")
    badges = []
    if attended_count >= 1: badges.append(("🎯", "First Step",       "Attended your first workshop"))
    if attended_count >= 3: badges.append(("🔥", "On a Streak",      "3+ workshops attended"))
    if fb_given     >= 2:   badges.append(("💬", "Feedback Hero",    "Shared feedback 2+ times"))
    if attended_count >= 5: badges.append(("🏆", "Lifelong Learner", "5+ workshops attended"))

    if not badges:
        st.info("Attend a workshop to earn your first badge!")
    else:
        cols = st.columns(min(4, len(badges)))
        for i, (icon, name, desc) in enumerate(badges):
            with cols[i % len(cols)]:
                st.markdown(
                    f"""
                    <div class="wiq-card" style="text-align:center;">
                        <div style="font-size:2rem;">{icon}</div>
                        <div style="font-weight:600;">{name}</div>
                        <div style="color:#6B7280; font-size:0.85rem;">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.divider()
    st.markdown("##### Preferences")
    st.checkbox("Email me weekly workshop digests", value=True)
    st.checkbox("Notify me about workshops in my interest areas", value=True)
    st.multiselect(
        "Interest areas",
        ["Technical", "Soft Skills", "Leadership", "Wellness"],
        default=["Technical", "Leadership"],
    )
    st.button("💾  Save preferences", type="primary")
