"""Login screen — no real auth, any input works."""

import streamlit as st
from styles import brand_header


def render():
    st.markdown('<div class="wiq-login-wrap">', unsafe_allow_html=True)
    brand_header("Sign in to continue")

    with st.container(border=True):
        st.markdown("#### Welcome back 👋")
        st.caption("Demo mode — any email and password will work.")

        email    = st.text_input("Work email", placeholder="you@acme.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        role     = st.radio(
            "Sign in as",
            options=["HR Admin", "Participant"],
            horizontal=True,
        )

        if st.button("Sign in", type="primary", width="stretch"):
            if not email:
                st.error("Please enter an email to continue.")
            else:
                st.session_state.auth["logged_in"] = True
                st.session_state.auth["role"]      = role
                st.session_state.auth["email"]     = email
                st.toast(f"Signed in as {role}", icon="✅")
                st.rerun()

    st.markdown(
        '<div style="text-align:center; color:#6B7280; font-size:0.8rem; margin-top:18px;">'
        'WorkshopIQ Demo · No data is stored beyond this session'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)
