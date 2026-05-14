# WorkshopIQ — Agentic AI Workshop Management (Demo)

A polished, **UI-only** Streamlit demo for an Agentic AI Workshop Management
System. No database, no real authentication, no real AI calls — every screen
is populated by in-memory mock data so a non-technical stakeholder can click
through and validate the concept before real development begins.

---

## What's inside

Two parallel experiences, gated by a simple role selector on the login screen:

**HR Admin Console**
- **Dashboard** — KPI cards, registrations-per-workshop bar chart, sentiment
  donut, and an upcoming workshops table.
- **Workshops** — searchable, filterable list of all workshops with a one-click
  drill-down.
- **Create Workshop** — form-based publish flow (title, date, facilitator,
  capacity, type, mode, …).
- **Workshop Details** — three tabs:
  - **Registrations** — confirmed attendees and waitlist.
  - **Facilitator Brief (AI)** — pre-canned themes, sentiment, concerns, and
    talking points distilled from registration inputs. Includes a
    "Regenerate Brief" button that simulates an AI call.
  - **Feedback & Insights** — average rating, distribution chart, raw
    comments, and an AI summary with positives / improvements / action items.
- **Participants** — full roster with no-show counts; flags frequent drop-offs.
- **Analytics** — attendance trend line, type-popularity bar, day × time
  heatmap, and a row of plain-English insight cards.
- **Settings** — mock email templates, reminder cadences, and integration
  status (Gmail, Calendar, Slack, Zoom, HRIS).

**Participant Portal**
- **Browse Workshops** — card grid with type chips and a "Register" CTA.
- **Register** — workshop detail page with a required "What do you hope to
  learn?" expectations field; submitting drops the registration into
  *My Workshops*.
- **My Workshops** — Upcoming (with Confirm / Can't Attend buttons) and Past
  (with an inline feedback form: 1–5 stars + comment).
- **Profile** — mock user card, attendance stats, and gamified badges.

---

## Run it locally

```bash
# 1. (Recommended) create and activate a virtualenv
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. install dependencies
pip install -r requirements.txt

# 3. launch the demo
streamlit run app.py
```

Streamlit will open the app in your browser at `http://localhost:8501`.

### Logging in

Any email + password works. Pick a role on the login screen:

- **HR Admin** lands you on the Dashboard with full admin nav.
- **Participant** lands you on Browse Workshops; you're stitched to a real
  mock participant under the hood so *My Workshops* looks populated from
  the first click.

Use the **Sign out** button at the bottom of the sidebar to switch roles.

---

## Project layout

```
workshop_management_demo/
├─ app.py                       # entry point: page config, login gate, router
├─ mock_data.py                 # all seed data + session_state init helpers
├─ styles.py                    # shared CSS, badges, KPI cards, empty states
├─ requirements.txt
├─ README.md
└─ pages_ui/                    # one render() function per major screen
   ├─ __init__.py
   ├─ login.py
   ├─ hr_dashboard.py
   ├─ hr_workshops.py
   ├─ hr_create_workshop.py
   ├─ hr_workshop_details.py
   ├─ hr_participants.py
   ├─ hr_analytics.py
   ├─ hr_settings.py
   ├─ participant_browse.py
   ├─ participant_register.py
   ├─ participant_my_workshops.py
   └─ participant_profile.py
```

Note: the folder is named `pages_ui/` (not `pages/`) on purpose — Streamlit's
multi-page auto-discovery would otherwise pick up every file in a top-level
`pages/` directory and add them to the sidebar. We handle routing manually
from `app.py` so the nav stays role-aware.

---

## Mock data

Seeded on first load via `mock_data.init_session_state()`:

- **5 facilitators** with realistic expertise areas.
- **36 participants** with realistic Indian names spread across 8
  departments.
- **10 workshops** spanning past and upcoming, across all four types
  (Technical / Soft Skills / Leadership / Wellness) and modes.
- **Registrations** populated at 55–95% of capacity per workshop, with
  attendance status (Confirmed / Pending / Declined / No-show) skewed
  realistically.
- **Feedback** entries (5–10 per past workshop) with mixed but generally
  positive ratings.
- **4 pre-canned AI facilitator briefs** and **3 AI feedback summaries**,
  rotated per workshop so screens look different without needing a model.

All in-session edits (new workshops, new registrations, new feedback) live
in `st.session_state` for the life of the browser tab and reset on reload.

---

## Design notes

- **Visual style.** Indigo/violet primary palette, rounded cards with soft
  shadows, status badges in green / amber / red, and emoji icons used
  sparingly. All defined in `styles.py` so it's easy to retheme.
- **Simulated AI delays.** "Regenerate Brief" and the registration confirm
  flow use `st.spinner()` / `st.balloons()` so the demo *feels* like it's
  doing AI work without actually doing any.
- **Friendly empty states.** Empty tabs and filtered-to-nothing views
  render a centered illustration + helpful nudge instead of a blank
  panel.
- **No persistence.** Everything is in-memory. This is intentional — the
  demo is meant to validate the *experience*, not to be a working product.
