"""HR Admin — Settings (placeholder UI)."""

import streamlit as st


def render():
    st.markdown("### Settings")
    st.caption("Configure workspace defaults, templates, and integrations")

    tab1, tab2, tab3 = st.tabs(["📧  Email templates", "⏰  Reminders", "🔌  Integrations"])

    with tab1:
        st.markdown("##### Registration confirmation")
        st.text_area(
            "Subject",
            value="You're in: {{workshop_title}} on {{date}}",
            key="tpl_conf_subject",
        )
        st.text_area(
            "Body",
            value=(
                "Hi {{first_name}},\n\n"
                "You're confirmed for {{workshop_title}} on {{date}} at {{time}}.\n"
                "Calendar invite attached. Reply if you have any questions.\n\n"
                "— The WorkshopIQ team"
            ),
            height=160,
            key="tpl_conf_body",
        )
        st.button("💾  Save template", type="primary", key="save_conf")

        st.divider()
        st.markdown("##### Post-workshop feedback request")
        st.text_area(
            "Subject ",
            value="Quick favor: 2-minute feedback on {{workshop_title}}",
            key="tpl_fb_subject",
        )
        st.button("💾  Save template", type="primary", key="save_fb")

    with tab2:
        st.markdown("##### When should we nudge participants?")
        st.checkbox("Send confirmation on registration", value=True)
        st.checkbox("Send reminder 24 hours before", value=True)
        st.checkbox("Send reminder 1 hour before", value=True)
        st.checkbox("Send feedback request 4 hours after", value=True)
        st.select_slider(
            "No-show follow-up",
            options=["Off", "Same day", "Next day", "Weekly digest"],
            value="Next day",
        )
        st.button("💾  Save reminder settings", type="primary", key="save_rem")

    with tab3:
        st.markdown("##### Connected services")

        def integration_row(name, status, icon):
            color = "#1F7A45" if status == "Connected" else "#B91C1C"
            symbol = "✓" if status == "Connected" else "✕"
            st.markdown(
                f"""
                <div class="wiq-card" style="display:flex; align-items:center; justify-content:space-between;">
                  <div>
                    <div style="font-weight:600;">{icon} &nbsp; {name}</div>
                    <div style="color:#6B7280; font-size:0.85rem;">
                        {'Synced 12 minutes ago' if status=='Connected' else 'Not connected'}
                    </div>
                  </div>
                  <div style="color:{color}; font-weight:600;">{symbol} &nbsp; {status}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        integration_row("Gmail",          "Connected",     "📧")
        integration_row("Google Calendar","Connected",     "📅")
        integration_row("Slack",          "Connected",     "💬")
        integration_row("Zoom",           "Connected",     "🎥")
        integration_row("HRIS (BambooHR)","Not connected", "🏢")
