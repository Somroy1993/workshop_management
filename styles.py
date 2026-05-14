"""
Shared CSS + small UI helpers used across pages.
Keeping all of this in one place so the look stays consistent.
"""

import streamlit as st

PRIMARY      = "#5B5BD6"   # indigo/violet
PRIMARY_DARK = "#3F3FB3"
ACCENT       = "#8B5CF6"
BG_SOFT      = "#F5F4FB"
TEXT_DIM     = "#6B7280"

BADGE_COLORS = {
    # Workshop / registration statuses
    "Upcoming":      ("#E8F1FF", "#1D4ED8"),
    "Starting Soon": ("#FFF4E5", "#B45309"),
    "Completed":     ("#ECECEC", "#4B5563"),
    "Confirmed":     ("#E6F7EC", "#1F7A45"),
    "Pending":       ("#FFF4E5", "#B45309"),
    "Declined":      ("#FCEBEB", "#B91C1C"),
    "No-show":       ("#FCEBEB", "#B91C1C"),
    # Mode
    "Virtual":       ("#EEF2FF", "#4338CA"),
    "In-person":     ("#ECFDF5", "#047857"),
    "Hybrid":        ("#FEF3C7", "#92400E"),
}


def inject_global_css():
    st.markdown(
        f"""
        <style>
            /* ----- Layout polish ----- */
            .block-container {{
                padding-top: 1.5rem;
                padding-bottom: 4rem;
                max-width: 1300px;
            }}

            /* ----- Header / brand ----- */
            .wiq-brand {{
                display: flex;
                align-items: center;
                gap: 0.6rem;
                margin-bottom: 0.5rem;
            }}
            .wiq-logo {{
                width: 38px; height: 38px;
                border-radius: 10px;
                background: linear-gradient(135deg, {PRIMARY} 0%, {ACCENT} 100%);
                color: #fff;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
                font-size: 18px;
                box-shadow: 0 4px 12px rgba(91,91,214,0.25);
            }}
            .wiq-name {{
                font-size: 1.35rem;
                font-weight: 700;
                color: #111827;
                letter-spacing: -0.02em;
            }}
            .wiq-tagline {{
                color: {TEXT_DIM};
                font-size: 0.85rem;
                margin-top: -2px;
            }}

            /* ----- Cards ----- */
            .wiq-card {{
                background: #ffffff;
                border: 1px solid #ECECF1;
                border-radius: 14px;
                padding: 18px 20px;
                box-shadow: 0 2px 8px rgba(17, 24, 39, 0.04);
                margin-bottom: 14px;
            }}
            .wiq-card-title {{
                font-weight: 600;
                font-size: 1rem;
                color: #111827;
                margin-bottom: 4px;
            }}
            .wiq-card-sub {{
                color: {TEXT_DIM};
                font-size: 0.85rem;
            }}

            /* ----- KPI cards ----- */
            .wiq-kpi {{
                background: #ffffff;
                border: 1px solid #ECECF1;
                border-radius: 14px;
                padding: 18px 20px;
                box-shadow: 0 2px 8px rgba(17, 24, 39, 0.04);
            }}
            .wiq-kpi-label {{
                color: {TEXT_DIM};
                font-size: 0.8rem;
                letter-spacing: 0.04em;
                text-transform: uppercase;
                font-weight: 600;
            }}
            .wiq-kpi-value {{
                font-size: 1.8rem;
                font-weight: 700;
                color: #111827;
                margin-top: 6px;
            }}
            .wiq-kpi-delta {{
                color: #047857;
                font-size: 0.8rem;
                font-weight: 600;
            }}

            /* ----- Badges ----- */
            .wiq-badge {{
                display: inline-block;
                padding: 3px 10px;
                border-radius: 999px;
                font-size: 0.75rem;
                font-weight: 600;
                line-height: 1.2;
            }}

            /* ----- AI insight card ----- */
            .wiq-ai-card {{
                background: linear-gradient(135deg, #F5F4FB 0%, #FFFFFF 100%);
                border: 1px solid #DCD8F0;
                border-radius: 14px;
                padding: 20px 22px;
                margin-bottom: 14px;
                position: relative;
            }}
            .wiq-ai-pill {{
                position: absolute;
                top: 14px; right: 16px;
                background: {PRIMARY};
                color: white;
                font-size: 0.7rem;
                font-weight: 600;
                padding: 3px 10px;
                border-radius: 999px;
                letter-spacing: 0.04em;
            }}
            .wiq-ai-section-title {{
                font-weight: 600;
                color: {PRIMARY_DARK};
                font-size: 0.78rem;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                margin-top: 12px;
                margin-bottom: 6px;
            }}
            .wiq-ai-card ul {{ margin: 0 0 0 1.2rem; padding: 0; }}
            .wiq-ai-card li {{ margin-bottom: 4px; }}

            /* ----- Workshop card (grid) ----- */
            .wiq-ws-card {{
                background: #ffffff;
                border: 1px solid #ECECF1;
                border-radius: 16px;
                padding: 18px 20px;
                box-shadow: 0 2px 8px rgba(17,24,39,0.04);
                height: 100%;
                display: flex;
                flex-direction: column;
                gap: 6px;
            }}
            .wiq-ws-title {{ font-weight: 700; font-size: 1.02rem; color: #111827; }}
            .wiq-ws-meta  {{ color: {TEXT_DIM}; font-size: 0.85rem; }}

            /* ----- Buttons ----- */
            .stButton > button[kind="primary"] {{
                background-color: {PRIMARY};
                border-color: {PRIMARY};
            }}
            .stButton > button[kind="primary"]:hover {{
                background-color: {PRIMARY_DARK};
                border-color: {PRIMARY_DARK};
            }}

            /* ----- Login page ----- */
            .wiq-login-wrap {{
                max-width: 420px;
                margin: 4rem auto 0 auto;
            }}

            /* Hide default Streamlit chrome we don't need */
            #MainMenu {{ visibility: hidden; }}
            footer    {{ visibility: hidden; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def brand_header(tagline: str = "Agentic AI for Workshop Management"):
    st.markdown(
        f"""
        <div class="wiq-brand">
            <div class="wiq-logo">W</div>
            <div>
                <div class="wiq-name">WorkshopIQ</div>
                <div class="wiq-tagline">{tagline}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def badge(label: str) -> str:
    """Return an HTML span you can drop into a markdown block."""
    bg, fg = BADGE_COLORS.get(label, ("#EEF2FF", "#4338CA"))
    return (
        f'<span class="wiq-badge" style="background:{bg};color:{fg};">{label}</span>'
    )


def kpi_card(label: str, value, delta: str | None = None):
    delta_html = f'<div class="wiq-kpi-delta">{delta}</div>' if delta else ""
    st.markdown(
        f"""
        <div class="wiq-kpi">
            <div class="wiq-kpi-label">{label}</div>
            <div class="wiq-kpi-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state(icon: str, title: str, body: str):
    st.markdown(
        f"""
        <div style="text-align:center; padding: 48px 16px; color:{TEXT_DIM};">
            <div style="font-size: 42px; margin-bottom: 8px;">{icon}</div>
            <div style="font-weight:600; color:#111827; margin-bottom:4px;">{title}</div>
            <div style="font-size:0.9rem;">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
