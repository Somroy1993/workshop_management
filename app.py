"""
WorkshopIQ — Agentic AI Workshop Management (UI-only demo).

Entry point. Handles:
  - page config + global CSS
  - one-time mock data seeding into st.session_state
  - login gate
  - sidebar nav (streamlit-option-menu) per role
  - manual page routing via st.session_state.current_page

Run with:
    streamlit run app.py
"""

import streamlit as st
from streamlit_option_menu import option_menu

from mock_data import init_session_state
from styles import inject_global_css, brand_header
from pages_ui import (
    login,
    hr_dashboard, hr_workshops, hr_create_workshop, hr_workshop_details,
    hr_participants, hr_analytics, hr_settings,
    participant_browse, participant_register,
    participant_my_workshops, participant_profile,
)


# ---------------------------------------------------------------------------
# Streamlit page config — must be the first Streamlit call.
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="WorkshopIQ",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()
init_session_state()


# ---------------------------------------------------------------------------
# Page registries — title → render function
# ---------------------------------------------------------------------------

HR_PAGES = {
    "Dashboard":         hr_dashboard.render,
    "Workshops":         hr_workshops.render,
    "Create Workshop":   hr_create_workshop.render,
    "Workshop Details":  hr_workshop_details.render,
    "Participants":      hr_participants.render,
    "Analytics":         hr_analytics.render,
    "Settings":          hr_settings.render,
}

PARTICIPANT_PAGES = {
    "Browse Workshops":  participant_browse.render,
    "Register":          participant_register.render,
    "My Workshops":      participant_my_workshops.render,
    "Profile":           participant_profile.render,
}

# Items that show up in the sidebar nav (a subset — drill-down pages
# like "Workshop Details" and "Register" are reached via buttons).
HR_NAV = [
    ("Dashboard",       "speedometer2"),
    ("Workshops",       "calendar-event"),
    ("Create Workshop", "plus-square"),
    ("Participants",    "people"),
    ("Analytics",       "graph-up"),
    ("Settings",        "gear"),
]

PARTICIPANT_NAV = [
    ("Browse Workshops", "search"),
    ("My Workshops",     "bookmark-check"),
    ("Profile",          "person-circle"),
]


# ---------------------------------------------------------------------------
# Sidebar (only shown after login)
# ---------------------------------------------------------------------------

def _render_sidebar(role: str):
    with st.sidebar:
        brand_header("Demo build")
        st.write("")

        nav   = HR_NAV if role == "HR Admin" else PARTICIPANT_NAV
        pages = HR_PAGES if role == "HR Admin" else PARTICIPANT_PAGES
        default_page = nav[0][0]

        # Keep the menu in sync with current_page when navigation happens
        # via in-page buttons (e.g., clicking "Open" on a workshop).
        current = st.session_state.get("current_page") or default_page
        menu_items = [name for name, _ in nav]
        # If we're on a drill-down page that's not in the nav, highlight
        # the nearest parent so the sidebar doesn't look unselected.
        if current not in menu_items:
            parent_map = {
                "Workshop Details": "Workshops",
                "Register":         "Browse Workshops",
            }
            highlight = parent_map.get(current, default_page)
        else:
            highlight = current

        try:
            highlight_idx = menu_items.index(highlight)
        except ValueError:
            highlight_idx = 0

        selection = option_menu(
            menu_title=None,
            options=menu_items,
            icons=[icon for _, icon in nav],
            default_index=highlight_idx,
            key=f"nav_{role}",
            styles={
                "container":   {"padding": "4px", "background-color": "transparent"},
                "icon":        {"color": "#5B5BD6", "font-size": "16px"},
                "nav-link":    {
                    "font-size":  "14px",
                    "text-align": "left",
                    "margin":     "4px 0",
                    "padding":    "10px 14px",
                    "border-radius": "10px",
                    "--hover-color": "#F5F4FB",
                },
                "nav-link-selected": {
                    "background-color": "#5B5BD6",
                    "color":             "white",
                    "font-weight":       "600",
                },
            },
        )

        # Sync sidebar choice -> current_page. Only treat it as a navigation
        # event if the user actually clicked something different from the
        # current page (otherwise drill-down clicks would get clobbered on
        # rerun).
        if selection != highlight:
            st.session_state.current_page = selection
            st.session_state.selected_workshop_id = None
            st.rerun()

        st.divider()

        # Footer: user info + sign out
        st.markdown(
            f"""
            <div style="color:#6B7280; font-size:0.85rem;">
                Signed in as<br>
                <strong style="color:#111827;">{st.session_state.auth['email']}</strong><br>
                <span style="font-size:0.75rem;">{role}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        if st.button("🚪  Sign out", width="stretch"):
            st.session_state.auth = {
                "logged_in":       False,
                "role":            None,
                "email":           None,
                "participant_id":  st.session_state.auth["participant_id"],
            }
            st.session_state.current_page = None
            st.rerun()


# ---------------------------------------------------------------------------
# Main router
# ---------------------------------------------------------------------------

def main():
    auth = st.session_state.auth

    if not auth["logged_in"]:
        login.render()
        return

    role  = auth["role"]
    pages = HR_PAGES if role == "HR Admin" else PARTICIPANT_PAGES

    # Default landing page per role
    if not st.session_state.get("current_page"):
        st.session_state.current_page = (
            "Dashboard" if role == "HR Admin" else "Browse Workshops"
        )

    _render_sidebar(role)

    page_name = st.session_state.current_page
    render_fn = pages.get(page_name)
    if not render_fn:
        st.error(f"Unknown page: {page_name}")
        return

    # Top-level brand strip (above each page's content)
    brand_header(
        "HR Admin Console" if role == "HR Admin" else "Participant Portal"
    )
    st.divider()

    render_fn()


if __name__ == "__main__":
    main()
