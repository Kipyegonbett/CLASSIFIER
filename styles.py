"""styles.py — improved UI with proper visibility & contrast"""

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Mono&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Base ── */
:root {
  --teal: #0d6e6e;
  --teal-dark: #094f4f;
  --cream: #f5f1eb;
  --ink: #111918;
  --muted: #5a6b69;
  --border: #cdd8d6;
  --danger: #c0392b;
  --green: #1a7a4a;
  --gold: #b59a5a;
}

/* Hide Streamlit UI */
#MainMenu, footer, header { visibility: hidden; }

/* App background */
.stApp {
  background: var(--cream) !important;
  font-family: 'DM Sans', sans-serif;
}

/* ── Card ── */
.auth-card {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 2rem;
  max-width: 450px;
  margin: auto;
}

/* ── Typography ── */
.card-title {
  font-family: 'DM Serif Display', serif;
  font-size: 1.6rem;
  color: var(--ink);
}

.card-sub {
  color: var(--muted);
  font-size: 0.9rem;
}

/* ── FIXED INPUT STYLING ── */
[data-testid="stTextInput"] input,
[data-testid="stPassword"] input,
textarea {
  background: #ffffff !important;
  color: var(--ink) !important;
  border: 1.5px solid var(--border) !important;
  border-radius: 8px !important;
  padding: 10px !important;
  font-size: 0.9rem !important;
}

/* Focus state */
[data-testid="stTextInput"] input:focus {
  border-color: var(--teal) !important;
  box-shadow: 0 0 0 2px rgba(13,110,110,0.15) !important;
}

/* ── LABEL FIX (MAIN ISSUE FIXED) ── */
label,
[data-testid="stTextInput"] label,
[data-testid="stPassword"] label {
  color: var(--ink) !important;
  font-weight: 500 !important;
  font-size: 0.9rem !important;
}

/* ── Placeholder ── */
::placeholder {
  color: #6b7280 !important;
  opacity: 1 !important;
}

/* ── Buttons ── */
.stButton > button {
  background: var(--teal-dark) !important;
  color: #fff !important;
  border-radius: 8px !important;
  padding: 10px !important;
  font-weight: 500 !important;
}

.stButton > button:hover {
  background: var(--teal) !important;
}

/* ── Alerts ── */
.alert {
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 10px;
}

.alert-danger  { background:#fde8e8; color:#7b1d1d; }
.alert-success { background:#d4f0e4; color:#0f4e2d; }
.alert-warning { background:#fff3cd; color:#5c420d; }
.alert-info    { background:#d0eeff; color:#0d3d5c; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
  background: var(--teal-dark) !important;
}

section[data-testid="stSidebar"] * {
  color: #ffffff !important;
}

/* ── Banner ── */
.portal-banner {
  background: var(--teal-dark);
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 1rem;
}

.banner-title {
  color: #fff;
  font-size: 1.5rem;
  font-family: 'DM Serif Display', serif;
}

.banner-sub {
  color: rgba(255,255,255,0.7);
  font-size: 0.9rem;
}

</style>
"""

def inject():
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def banner(title, subtitle):
    import streamlit as st
    st.markdown(f"""
    <div class="portal-banner">
        <div class="banner-title">{title}</div>
        <div class="banner-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def alert(msg, kind="danger"):
    import streamlit as st
    st.markdown(f"""
    <div class="alert alert-{kind}">
        {msg}
    </div>
    """, unsafe_allow_html=True)
