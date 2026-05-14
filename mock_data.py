"""
Mock seed data for the WorkshopIQ demo.

All data is generated as plain Python dicts/lists and loaded into
st.session_state on first run by `init_session_state()`. No persistence,
no real services — this is a UI-only demo.
"""

from datetime import datetime, timedelta, time
import random
import streamlit as st


# ---------------------------------------------------------------------------
# Static reference data
# ---------------------------------------------------------------------------

FACILITATORS = [
    {"id": "f1", "name": "Dr. Priya Sharma",   "expertise": "Leadership & Coaching"},
    {"id": "f2", "name": "Arjun Mehta",        "expertise": "Cloud & DevOps"},
    {"id": "f3", "name": "Kavya Nair",         "expertise": "Mindfulness & Wellness"},
    {"id": "f4", "name": "Rohit Iyer",         "expertise": "Data Science & AI"},
    {"id": "f5", "name": "Ananya Deshmukh",    "expertise": "Communication Skills"},
]

DEPARTMENTS = [
    "Engineering", "Product", "Design", "Marketing",
    "Sales", "People Ops", "Finance", "Customer Success",
]

WORKSHOP_TYPES   = ["Technical", "Soft Skills", "Leadership", "Wellness"]
WORKSHOP_MODES   = ["Virtual", "In-person", "Hybrid"]

# Realistic Indian first/last names for participant generation
FIRST_NAMES = [
    "Aarav", "Vihaan", "Aditya", "Vivaan", "Arjun", "Reyansh", "Krishna", "Ishaan",
    "Shaurya", "Atharv", "Ayaan", "Kabir", "Anaya", "Aadhya", "Diya", "Pari",
    "Ananya", "Saanvi", "Myra", "Aarohi", "Kiara", "Anika", "Riya", "Navya",
    "Tara", "Ira", "Aryan", "Devansh", "Rudra", "Veer", "Kunal", "Neha",
    "Pooja", "Shreya", "Sneha", "Priya", "Meera", "Kavya", "Nisha", "Ritu",
]

LAST_NAMES = [
    "Sharma", "Verma", "Iyer", "Nair", "Reddy", "Kapoor", "Khanna", "Mehta",
    "Bose", "Chatterjee", "Patel", "Gupta", "Joshi", "Desai", "Pillai",
    "Rao", "Singh", "Banerjee", "Krishnan", "Menon",
]


# ---------------------------------------------------------------------------
# Pre-canned AI outputs — rotated per workshop so screens look populated
# without needing a real model.
# ---------------------------------------------------------------------------

FACILITATOR_BRIEFS = [
    {
        "top_themes": [
            "Bridging the gap between theory and day-to-day project work",
            "Career growth for mid-level individual contributors",
            "Hands-on examples over slide-heavy content",
        ],
        "sentiment_summary": (
            "Participants are broadly enthusiastic and arrive with concrete questions. "
            "A small cohort signals mild anxiety about pace — consider a brief warm-up."
        ),
        "key_concerns": [
            "Workshop running over time and cutting into other commitments",
            "Content being too introductory for senior attendees",
            "Lack of follow-up resources after the session",
        ],
        "talking_points": [
            "Open with a 2-minute audience poll to gauge experience levels",
            "Anchor each concept with a real customer scenario",
            "Reserve last 10 minutes for an explicit Q&A — not crammed at the end",
            "Share a follow-up resource pack within 24 hours",
        ],
    },
    {
        "top_themes": [
            "Practical frameworks people can use the very next day",
            "Confidence in giving and receiving difficult feedback",
            "Managing up without overstepping",
        ],
        "sentiment_summary": (
            "Tone is curious and slightly cautious. Several participants mentioned past "
            "workshops that 'didn't stick' — they want tools, not theory."
        ),
        "key_concerns": [
            "Generic advice that doesn't apply to their team context",
            "Role-play exercises feeling forced",
            "Discomfort sharing sensitive examples in a group setting",
        ],
        "talking_points": [
            "Frame role-plays as low-stakes rehearsal, not performance",
            "Use anonymized real examples sourced from intake forms",
            "Offer a 1:1 follow-up option for sensitive conversations",
            "Close with a written commitment exercise",
        ],
    },
    {
        "top_themes": [
            "Burnout signals and recovery practices",
            "Building micro-habits that survive busy weeks",
            "Boundaries around always-on culture",
        ],
        "sentiment_summary": (
            "Group skews tired but optimistic. Strong appetite for techniques that "
            "fit a 5-minute window between meetings."
        ),
        "key_concerns": [
            "Feeling like 'wellness' is performative",
            "Lack of leadership buy-in for taking breaks",
            "Privacy when sharing personal struggles",
        ],
        "talking_points": [
            "Acknowledge cynicism up front — don't paper over it",
            "Share data on how short resets compound",
            "Demonstrate one technique live, then practice in pairs",
            "End with one habit each person will try this week",
        ],
    },
    {
        "top_themes": [
            "Going from prototype to production-grade systems",
            "Choosing the right abstraction level",
            "Debugging when the stack trace doesn't help",
        ],
        "sentiment_summary": (
            "Highly engaged technical audience. Expect sharp questions and a few "
            "'well actually' moments — lean into them."
        ),
        "key_concerns": [
            "Examples being too toy-like to be useful",
            "Glossing over edge cases and failure modes",
            "Missing trade-off discussion vs. competing approaches",
        ],
        "talking_points": [
            "Use a single non-trivial example throughout — no toy snippets",
            "Show at least one thing that went wrong and how it was fixed",
            "Explicitly compare against 1–2 alternative approaches",
            "Share the runnable repo before the session, not after",
        ],
    },
]

FEEDBACK_SUMMARIES = [
    {
        "top_positives": [
            "Facilitator's energy kept the group engaged across the full session",
            "Concrete examples from real projects landed well",
            "Pace was well-judged — no one felt rushed or held back",
        ],
        "top_improvements": [
            "More time needed for hands-on exercises",
            "A few slides were text-heavy and hard to read on smaller screens",
            "Pre-reading would have helped junior attendees keep up",
        ],
        "action_items": [
            "Trim slides by 20% and replace bullets with diagrams",
            "Send a 1-page primer 48 hours before next session",
            "Add a dedicated 15-minute lab block",
        ],
    },
    {
        "top_positives": [
            "Practical frameworks people could apply immediately",
            "Small-group breakouts made it safe to be honest",
            "Q&A felt genuine — facilitator engaged with hard questions",
        ],
        "top_improvements": [
            "Virtual attendees felt slightly disconnected from in-room energy",
            "Some examples skewed to engineering — broaden across functions",
            "Recording was not shared promptly",
        ],
        "action_items": [
            "Assign a dedicated remote-attendee host next time",
            "Curate examples from 3 different functions",
            "Publish recording within 24h via the People Ops portal",
        ],
    },
    {
        "top_positives": [
            "Felt restorative without being preachy",
            "Techniques were realistic for a packed workday",
            "Facilitator created a non-judgmental space",
        ],
        "top_improvements": [
            "Would like a follow-up session in 4–6 weeks",
            "Audio quality dipped during the meditation portion",
            "Workbook PDF had a broken link",
        ],
        "action_items": [
            "Schedule a follow-up cohort session for the same group",
            "Test audio with the meditation track before going live",
            "Fix workbook link and re-share",
        ],
    },
]


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------

def _seed_participants(n=36):
    rng = random.Random(42)
    used = set()
    participants = []
    i = 1
    while len(participants) < n:
        first = rng.choice(FIRST_NAMES)
        last  = rng.choice(LAST_NAMES)
        full  = f"{first} {last}"
        if full in used:
            continue
        used.add(full)
        participants.append({
            "id":         f"p{i:03d}",
            "name":       full,
            "email":      f"{first.lower()}.{last.lower()}@acme.com",
            "department": rng.choice(DEPARTMENTS),
        })
        i += 1
    return participants


def _seed_workshops(today):
    """
    Returns a mix of past and upcoming workshops. Dates are anchored to
    `today` so the demo always shows a believable spread regardless of when
    it's run.
    """
    rng = random.Random(7)

    specs = [
        # (title,                                       days_offset, type,          mode,        duration_min, capacity, facilitator_idx)
        ("Leading Through Ambiguity",                   -42,  "Leadership",  "Hybrid",     90,  40, 0),
        ("Intro to LLM-Powered Applications",           -28,  "Technical",   "Virtual",   120,  60, 3),
        ("Mindful Mondays: Reset & Refocus",            -21,  "Wellness",    "Virtual",    60,  50, 2),
        ("Giving Feedback That Sticks",                 -14,  "Soft Skills", "In-person",  90,  30, 4),
        ("Production-Ready Kubernetes",                  -7,  "Technical",   "Hybrid",    180,  35, 1),
        ("Storytelling for Engineers",                    5,  "Soft Skills", "Virtual",    90,  45, 4),
        ("Coaching Conversations for Managers",          12,  "Leadership",  "In-person", 120,  25, 0),
        ("Hands-on: RAG Systems with Evaluations",       19,  "Technical",   "Hybrid",    150,  40, 3),
        ("Stress, Sleep & Recovery",                     26,  "Wellness",    "Virtual",    60,  80, 2),
        ("Influencing Without Authority",                33,  "Soft Skills", "In-person",  90,  30, 4),
    ]

    workshops = []
    for idx, (title, offset, wtype, mode, duration, capacity, fac_idx) in enumerate(specs, start=1):
        wdate = today + timedelta(days=offset)
        is_past = offset < 0
        workshops.append({
            "id":           f"w{idx:03d}",
            "title":        title,
            "description":  _description_for(title, wtype),
            "date":         wdate,
            "time":         time(rng.choice([10, 11, 14, 15, 16]), rng.choice([0, 30])),
            "duration_min": duration,
            "facilitator_id": FACILITATORS[fac_idx]["id"],
            "type":         wtype,
            "mode":         mode,
            "capacity":     capacity,
            "status":       "Completed" if is_past else ("Upcoming" if offset > 2 else "Starting Soon"),
            "is_past":      is_past,
            # Pre-canned outputs rotated by index
            "brief_idx":    idx % len(FACILITATOR_BRIEFS),
            "summary_idx":  idx % len(FEEDBACK_SUMMARIES),
        })
    return workshops


def _description_for(title, wtype):
    base = {
        "Technical": (
            "A practical, code-first session. Bring a laptop. We'll work through "
            "a realistic example end-to-end with room for questions throughout."
        ),
        "Soft Skills": (
            "An interactive session with short frameworks and small-group practice. "
            "Come ready to participate — there are no slides-only sections."
        ),
        "Leadership": (
            "Designed for people who lead others (formally or informally). Expect "
            "real scenarios, honest discussion, and one tool you can use this week."
        ),
        "Wellness": (
            "A calm, judgement-free session focused on techniques that fit into a "
            "busy workday. No prior experience needed."
        ),
    }
    return base[wtype] + f"\n\nWorkshop: {title}."


def _seed_registrations(workshops, participants):
    """
    For each workshop, register a believable fraction of participants.
    Past workshops also get an attendance status; upcoming ones get
    Confirmed / Pending.
    """
    rng = random.Random(99)
    registrations = []
    for w in workshops:
        # Cap by both capacity and participant pool size — some workshops
        # have a larger capacity than the total number of seeded people.
        target = rng.randint(int(w["capacity"] * 0.55), int(w["capacity"] * 0.95))
        n_reg = min(w["capacity"], len(participants), target)
        attendees = rng.sample(participants, n_reg)
        for p in attendees:
            if w["is_past"]:
                # Attendance distribution: mostly confirmed, some no-shows
                status = rng.choices(
                    ["Confirmed", "No-show", "Declined"],
                    weights=[80, 15, 5],
                )[0]
            else:
                status = rng.choices(
                    ["Confirmed", "Pending"],
                    weights=[70, 30],
                )[0]
            registrations.append({
                "id":            f"r-{w['id']}-{p['id']}",
                "workshop_id":   w["id"],
                "participant_id": p["id"],
                "registered_on": w["date"] - timedelta(days=rng.randint(2, 21)),
                "expectations":  rng.choice(EXPECTATIONS),
                "status":        status,
            })
    return registrations


EXPECTATIONS = [
    "Hoping to pick up frameworks I can apply with my team next week.",
    "Want to understand where this fits in our broader roadmap.",
    "I've struggled with this in 1:1s — looking for concrete language.",
    "Curious about how others outside my function approach this.",
    "Need a refresher — last did formal training a few years ago.",
    "Want to bring back ideas to share with my squad.",
    "Hoping for hands-on practice, not just lecture.",
    "Trying to decide whether to go deeper in this area.",
    "",  # some participants leave it blank
]


def _seed_feedback(workshops, registrations):
    """
    5–10 feedback entries per past workshop, with mixed but generally
    positive ratings (skewed toward 4–5).
    """
    rng = random.Random(123)
    feedback = []
    comments_pool = [
        "Loved the practical examples — felt directly applicable.",
        "Facilitator was clearly knowledgeable but moved a bit fast for me.",
        "The breakout discussions were the highlight.",
        "Would have liked more time for Q&A.",
        "Slides were a bit dense, but the verbal explanation was great.",
        "Best workshop I've attended this year. Please do a follow-up.",
        "Useful, though some content overlapped with last month's session.",
        "Not sure the role-play landed for me — felt slightly forced.",
        "Energy was excellent. Walked out with a clear next step.",
        "Audio on the virtual side had issues. Please test before.",
        "Strong intro, weaker close — felt rushed at the end.",
        "Hands-on portion was perfectly pitched.",
    ]

    for w in workshops:
        if not w["is_past"]:
            continue
        attended = [r for r in registrations if r["workshop_id"] == w["id"] and r["status"] == "Confirmed"]
        n_fb = min(len(attended), rng.randint(5, 10))
        for r in rng.sample(attended, n_fb):
            rating = rng.choices([3, 4, 5], weights=[15, 45, 40])[0]
            feedback.append({
                "id":             f"fb-{r['id']}",
                "workshop_id":    w["id"],
                "participant_id": r["participant_id"],
                "rating":         rating,
                "comment":        rng.choice(comments_pool),
                "submitted_on":   w["date"] + timedelta(days=rng.randint(1, 3)),
            })
    return feedback


# ---------------------------------------------------------------------------
# Public: initialize st.session_state on first load
# ---------------------------------------------------------------------------

def init_session_state():
    """Idempotent. Safe to call on every rerun."""
    if st.session_state.get("_seeded"):
        return

    today = datetime.now().date()

    facilitators = FACILITATORS[:]
    participants = _seed_participants(36)
    workshops    = _seed_workshops(today)
    registrations = _seed_registrations(workshops, participants)
    feedback     = _seed_feedback(workshops, registrations)

    st.session_state.facilitators  = facilitators
    st.session_state.participants  = participants
    st.session_state.workshops     = workshops
    st.session_state.registrations = registrations
    st.session_state.feedback      = feedback

    # Auth + nav state
    st.session_state.auth = {
        "logged_in": False,
        "role":      None,
        "email":     None,
        # For the participant view, pretend the logged-in user is a real
        # person from the participants list so "My Workshops" looks populated.
        "participant_id": participants[0]["id"],
    }

    st.session_state.current_page    = None
    st.session_state.selected_workshop_id = None
    st.session_state.brief_regenerated_at = {}

    st.session_state._seeded = True


# ---------------------------------------------------------------------------
# Convenience accessors used by page modules
# ---------------------------------------------------------------------------

def get_facilitator(fid):
    return next((f for f in st.session_state.facilitators if f["id"] == fid), None)


def get_participant(pid):
    return next((p for p in st.session_state.participants if p["id"] == pid), None)


def get_workshop(wid):
    return next((w for w in st.session_state.workshops if w["id"] == wid), None)


def registrations_for(workshop_id):
    return [r for r in st.session_state.registrations if r["workshop_id"] == workshop_id]


def feedback_for(workshop_id):
    return [f for f in st.session_state.feedback if f["workshop_id"] == workshop_id]


def workshops_for_participant(participant_id):
    reg_ids = {r["workshop_id"] for r in st.session_state.registrations
               if r["participant_id"] == participant_id}
    return [w for w in st.session_state.workshops if w["id"] in reg_ids]


def brief_for_workshop(workshop_id):
    w = get_workshop(workshop_id)
    return FACILITATOR_BRIEFS[w["brief_idx"]]


def summary_for_workshop(workshop_id):
    w = get_workshop(workshop_id)
    return FEEDBACK_SUMMARIES[w["summary_idx"]]
