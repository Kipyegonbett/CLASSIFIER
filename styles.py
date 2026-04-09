"""styles.py — shared CSS injected via st.markdown"""

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; }
:root {
  --teal:       #0d6e6e;
  --teal-light: #12908f;
  --teal-dark:  #094f4f;
  --cream:      #f5f1eb;
  --warm:       #faf8f5;
  --ink:        #111918;
  --muted:      #5a6b69;
  --border:     #cdd8d6;
  --danger:     #c0392b;
  --gold:       #b59a5a;
  --green:      #1a7a4a;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }

/* App background */
.stApp { background: var(--cream) !important; font-family: 'DM Sans', sans-serif; }
[data-testid="stAppViewContainer"] { background: var(--cream); }
[data-testid="stVerticalBlock"] { gap: 0 !important; }

/* ── Card wrapper ── */
.auth-card {
  background: #fff;
  border: 1.5px solid var(--border);
  border-radius: 18px;
  padding: 2.4rem 2.2rem;
  max-width: 460px;
  margin: 0 auto;
  box-shadow: 0 4px 32px rgba(9,79,79,0.07);
}

/* ── Header banner ── */
.portal-banner {
  background: var(--teal-dark);
  border-radius: 16px;
  padding: 2.2rem 2.4rem;
  margin-bottom: 1.6rem;
  position: relative;
  overflow: hidden;
}
.portal-banner::before {
  content: '';
  position: absolute; inset: 0;
  background:
    radial-gradient(ellipse 80% 60% at 15% 85%, rgba(18,144,143,.4) 0%, transparent 60%),
    radial-gradient(ellipse 50% 50% at 90% 10%, rgba(181,154,90,.2) 0%, transparent 55%);
}
.portal-banner::after {
  content: '';
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,.04) 1px, transparent 1px);
  background-size: 36px 36px;
}
.banner-inner { position: relative; z-index: 1; }
.banner-pill {
  display: inline-flex; align-items: center; gap: 7px;
  background: rgba(255,255,255,.12);
  border: 1px solid rgba(255,255,255,.2);
  border-radius: 30px; padding: 5px 14px;
  margin-bottom: .9rem;
}
.banner-pill .dot-green {
  width: 7px; height: 7px; border-radius: 50%;
  background: #4ade80; box-shadow: 0 0 6px #4ade80;
  animation: pulse 2s infinite;
}
.banner-pill span { font-family:'DM Mono',monospace; font-size:.68rem; letter-spacing:.1em; text-transform:uppercase; color:rgba(255,255,255,.8); }
.banner-title { font-family:'DM Serif Display',serif; font-size:1.9rem; color:#fff; line-height:1.2; margin-bottom:.5rem; }
.banner-title em { font-style:italic; color:var(--gold); }
.banner-sub { font-size:.84rem; color:rgba(255,255,255,.58); line-height:1.65; max-width:380px; }

/* ── Eyebrow ── */
.eyebrow {
  font-family:'DM Mono',monospace; font-size:.68rem; letter-spacing:.14em;
  text-transform:uppercase; color:var(--teal); margin-bottom:1rem;
  display:flex; align-items:center; gap:8px;
}
.eyebrow::before { content:''; display:block; width:22px; height:1.5px; background:var(--teal); }

/* ── Card title ── */
.card-title { font-family:'DM Serif Display',serif; font-size:1.75rem; color:var(--ink); margin-bottom:.35rem; }
.card-sub   { font-size:.84rem; color:var(--muted); margin-bottom:1.6rem; line-height:1.6; }

/* ── Streamlit input overrides ── */
[data-testid="stTextInput"] input,
[data-testid="stTextInput"] input:focus {
  border: 1.5px solid var(--border) !important;
  border-radius: 10px !important;
  font-size: .9rem !important;
  font-family: 'DM Sans', sans-serif !important;
  background: #fff !important;
  color: var(--ink) !important;
  padding: 11px 14px !important;
  box-shadow: none !important;
  transition: border-color .18s !important;
}
[data-testid="stTextInput"] input:focus {
  border-color: var(--teal) !important;
  box-shadow: 0 0 0 3px rgba(13,110,110,.1) !important;
}

/* ── Buttons ── */
.stButton > button {
  width: 100%;
  padding: 12px 20px !important;
  background: var(--teal-dark) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 10px !important;
  font-size: .92rem !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 500 !important;
  letter-spacing: .02em !important;
  cursor: pointer !important;
  transition: background .18s !important;
}
.stButton > button:hover { background: var(--teal) !important; }

/* ── Alerts ── */
.alert {
  border-radius: 10px; padding: 11px 15px;
  font-size: .82rem; line-height: 1.55;
  display: flex; align-items: flex-start; gap: 9px;
  margin-bottom: 1rem;
}
.alert-danger  { background:#fde8e8; border-left:3px solid var(--danger); color:#7b1d1d; }
.alert-success { background:#d4f0e4; border-left:3px solid var(--green);  color:#0f4e2d; }
.alert-warning { background:#fff3cd; border-left:3px solid #b07d2a;       color:#5c420d; }
.alert-info    { background:#d0eeff; border-left:3px solid #2575a8;       color:#0d3d5c; }

/* ── Notice box ── */
.notice {
  background: rgba(13,110,110,.06);
  border: 1px solid rgba(13,110,110,.2);
  border-radius: 10px; padding: 11px 14px;
  display: flex; gap: 10px; align-items: flex-start;
  margin-top: 1.2rem;
}
.notice p { font-size:.74rem; color:var(--teal-dark); line-height:1.55; margin:0; }
.notice strong { font-family:'DM Mono',monospace; font-size:.7rem; }

/* ── Nav link ── */
.nav-link { text-align:center; margin-top:1rem; font-size:.84rem; color:var(--muted); }
.nav-link a { color:var(--teal); font-weight:500; text-decoration:none; }
.nav-link a:hover { text-decoration:underline; }

/* ── Stat chips ── */
.stat-row { display:flex; gap:10px; margin:1.2rem 0; flex-wrap:wrap; }
.stat-chip {
  background: rgba(255,255,255,.1); border:1px solid rgba(255,255,255,.15);
  border-radius:10px; padding:10px 14px; text-align:center;
}
.stat-chip .sn { font-family:'DM Serif Display',serif; font-size:1.3rem; color:#fff; }
.stat-chip .sl { font-size:.62rem; color:rgba(255,255,255,.45); text-transform:uppercase; letter-spacing:.09em; }

/* ── Admin table ── */
.admin-table { width:100%; border-collapse:collapse; font-size:.84rem; }
.admin-table th {
  padding:9px 14px; text-align:left; font-size:.7rem; font-weight:500;
  color:var(--muted); text-transform:uppercase; letter-spacing:.08em;
  background:var(--cream); border-bottom:1px solid var(--border);
}
.admin-table td { padding:12px 14px; border-bottom:1px solid #f0ebe4; vertical-align:middle; }
.admin-table tr:last-child td { border-bottom:none; }

/* ── Status badges ── */
.sb { display:inline-flex;align-items:center;gap:5px;padding:3px 10px;border-radius:20px;font-size:.7rem;font-family:'DM Mono',monospace; }
.sb-pending  { background:#fef3c7;color:#92400e; }
.sb-approved { background:#d1fae5;color:#065f46; }
.sb-rejected { background:#fee2e2;color:#991b1b; }
.sb-forced   { background:#f3e8ff;color:#6b21a8; }
.sb-online   { background:#d1fae5;color:#065f46; }
.sb-offline  { background:#f1f5f9;color:#64748b; }

/* ── Section card ── */
.section-card {
  background:#fff; border:1px solid var(--border);
  border-radius:14px; overflow:hidden; margin-bottom:1.4rem;
}
.section-head {
  padding:1.1rem 1.4rem; border-bottom:1px solid var(--border);
  display:flex; align-items:center; justify-content:space-between;
}
.section-head h3 { font-size:.95rem; font-weight:600; color:var(--ink); margin:0; }
.count-badge {
  font-family:'DM Mono',monospace; font-size:.68rem;
  background:var(--cream); border:1px solid var(--border);
  border-radius:20px; padding:2px 10px; color:var(--muted);
}

/* ── Metric cards ── */
.metric-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin-bottom:1.6rem; }
.metric-card { background:#fff; border:1px solid var(--border); border-radius:14px; padding:1.2rem 1.3rem; }
.metric-card .mn { font-family:'DM Serif Display',serif; font-size:2rem; color:var(--ink); }
.metric-card .ml { font-size:.7rem; color:var(--muted); text-transform:uppercase; letter-spacing:.08em; margin-top:2px; }
.mc-pending  { border-left:3px solid #f59e0b; }
.mc-approved { border-left:3px solid var(--teal); }
.mc-rejected { border-left:3px solid var(--danger); }

/* ── Dashboard welcome ── */
.dash-welcome {
  background:var(--teal-dark); border-radius:16px; padding:2rem 2.2rem;
  position:relative; overflow:hidden; margin-bottom:1.4rem;
}
.dash-welcome::before { content:''; position:absolute; inset:0; background:radial-gradient(ellipse 70% 80% at 90% 50%,rgba(181,154,90,.2) 0%,transparent 60%); }
.dash-welcome::after  { content:''; position:absolute; inset:0; background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px); background-size:30px 30px; }
.dw-inner { position:relative; z-index:1; }
.dw-inner h2 { font-family:'DM Serif Display',serif; font-size:1.6rem; color:#fff; margin-bottom:.4rem; }
.dw-inner p  { font-size:.84rem; color:rgba(255,255,255,.6); line-height:1.65; max-width:500px; margin:0; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
  background: var(--teal-dark) !important;
  border-right: none !important;
}
section[data-testid="stSidebar"] * { color: rgba(255,255,255,.85) !important; }
section[data-testid="stSidebar"] .stButton > button {
  background: rgba(255,255,255,.1) !important;
  border: 1px solid rgba(255,255,255,.15) !important;
  color: rgba(255,255,255,.8) !important;
  border-radius: 8px !important;
  font-size: .82rem !important;
  padding: 8px 14px !important;
  width:100%;
}
section[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(220,50,50,.25) !important;
  color: #fca5a5 !important;
}
.sb-user-card {
  background:rgba(255,255,255,.09); border:1px solid rgba(255,255,255,.12);
  border-radius:12px; padding:.9rem 1rem; margin-bottom:1.2rem;
}
.sb-avatar {
  width:38px;height:38px;border-radius:50%;background:var(--teal-light);
  display:inline-flex;align-items:center;justify-content:center;
  font-family:'DM Serif Display',serif;font-size:1rem;color:#fff;margin-bottom:.5rem;
}
.sb-name  { font-size:.88rem; font-weight:500; color:#fff !important; }
.sb-email { font-family:'DM Mono',monospace; font-size:.6rem; color:rgba(255,255,255,.45) !important; word-break:break-all; }
.sb-role  { font-family:'DM Mono',monospace; font-size:.62rem; color:var(--gold) !important; text-transform:uppercase; letter-spacing:.09em; margin-top:.4rem; }

@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.5;transform:scale(.85)} }
</style>
"""


def inject():
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def banner(title_html: str, subtitle: str, pill: str = "hospital.ac.ke"):
    import streamlit as st
    st.markdown(f"""
    <div class="portal-banner">
      <div class="banner-inner">
        <div class="banner-pill">
          <div class="dot-green"></div>
          <span>{pill}</span>
        </div>
        <div class="banner-title">{title_html}</div>
        <div class="banner-sub">{subtitle}</div>
        <div class="stat-row">
          <div class="stat-chip"><div class="sn">ICD-11</div><div class="sl">Standard</div></div>
          <div class="stat-chip"><div class="sn">BioBERT</div><div class="sl">Model</div></div>
          <div class="stat-chip"><div class="sn">256</div><div class="sl">Max Tokens</div></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def alert(msg: str, kind: str = "danger"):
    import streamlit as st
    icons = {"danger": "⚠", "success": "✓", "warning": "!", "info": "ℹ"}
    st.markdown(f"""
    <div class="alert alert-{kind}">
      <span>{icons.get(kind,'•')}</span>
      <span>{msg}</span>
    </div>""", unsafe_allow_html=True)
