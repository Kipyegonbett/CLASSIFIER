"""
app.py — Clinical BioBERT Auth Portal (Streamlit)
Pages: register | signin | dashboard (user) | admin
Deploy: Streamlit Community Cloud from GitHub
"""

import streamlit as st
from werkzeug.security import generate_password_hash, check_password_hash

import db
import styles

# ── Page config ────────────────────────────────────────────────
st.set_page_config(
    page_title="Clinical BioBERT Portal",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed",
)

ALLOWED_DOMAIN = "@hospital.ac.ke"

# ── Init DB ────────────────────────────────────────────────────
db.init_db()

# ── Session defaults ───────────────────────────────────────────
for key, val in {
    "user": None,          # dict of logged-in user
    "page": "register",    # register | signin | dashboard | admin
    "flash": None,         # (msg, kind)
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Helpers ────────────────────────────────────────────────────
def go(page: str):
    st.session_state.page = page
    st.rerun()

def flash(msg: str, kind: str = "danger"):
    st.session_state.flash = (msg, kind)

def show_flash():
    if st.session_state.flash:
        msg, kind = st.session_state.flash
        styles.alert(msg, kind)
        st.session_state.flash = None

def logout():
    if st.session_state.user:
        db.record_logout(st.session_state.user["id"])
    st.session_state.user = None
    flash("You have been signed out.", "info")
    go("signin")

def sidebar_user():
    """Render the user info block in sidebar."""
    u = st.session_state.user
    if not u:
        return
    role_label = "Administrator" if u["role"] == "admin" else "Researcher"
    initial = u["name"][0].upper()
    with st.sidebar:
        st.markdown(f"""
        <div class="sb-user-card">
          <div class="sb-avatar">{initial}</div>
          <div class="sb-name">{u['name']}</div>
          <div class="sb-email">{u['email']}</div>
          <div class="sb-role">{role_label}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⏏  Sign out", key="sb_logout"):
            logout()

# ══════════════════════════════════════════════════════════════
#  PAGE: REGISTER
# ══════════════════════════════════════════════════════════════
def page_register():
    styles.inject()
    styles.banner(
        "Join the <em>Clinical BioBERT</em> Research Portal",
        "Create your institutional account to access ICD-11 AI coding tools. "
        "Accounts require admin approval before activation.",
    )

    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">New Account</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Create account</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-sub">Register with your hospital email. An administrator will review your request.</div>', unsafe_allow_html=True)

    show_flash()

    name     = st.text_input("Full Name",    placeholder="Dr. Jane Mwangi",           key="reg_name")
    email    = st.text_input("Institutional Email", placeholder="yourname@hospital.ac.ke", key="reg_email")
    password = st.text_input("Password",     placeholder="Min. 8 characters",          type="password", key="reg_pw")
    confirm  = st.text_input("Confirm Password", placeholder="Re-enter password",      type="password", key="reg_pw2")

    if st.button("Create Account", key="reg_submit"):
        errors = []
        if not name.strip():
            errors.append("Full name is required.")
        if not email.strip().lower().endswith(ALLOWED_DOMAIN):
            errors.append(f"Only {ALLOWED_DOMAIN} email addresses are allowed.")
        if len(password) < 8:
            errors.append("Password must be at least 8 characters.")
        if password != confirm:
            errors.append("Passwords do not match.")

        if errors:
            for e in errors:
                styles.alert(e, "danger")
        else:
            ok, err = db.create_user(
                name.strip(),
                email.strip().lower(),
                generate_password_hash(password),
            )
            if ok:
                flash("Account created! Please wait for admin approval before signing in.", "success")
                go("signin")
            else:
                styles.alert(err, "danger")

    st.markdown("""
    <div class="nav-link">Already have an account? <a href="#" onclick="void(0)">Sign in below ↓</a></div>
    """, unsafe_allow_html=True)

    if st.button("Go to Sign In →", key="reg_to_signin"):
        go("signin")

    st.markdown("""
    <div class="notice">
      <span>🔒</span>
      <p>Access restricted to <strong>@hospital.ac.ke</strong> addresses only.
      Accounts are manually reviewed before activation.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  PAGE: SIGN IN
# ══════════════════════════════════════════════════════════════
def page_signin():
    styles.inject()
    styles.banner(
        "Clinical <em>BioBERT</em> ICD-11 Coding",
        "AI-powered medical coding using BioBERT for accurate ICD-11 "
        "disease classification from clinical notes.",
    )

    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">Secure Access Portal</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Welcome back</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-sub">Sign in with your hospital institutional email.</div>', unsafe_allow_html=True)

    show_flash()

    email    = st.text_input("Institutional Email", placeholder="yourname@hospital.ac.ke", key="si_email")
    password = st.text_input("Password", placeholder="Enter your password", type="password", key="si_pw")

    if st.button("Sign in to Dashboard", key="si_submit"):
        em = email.strip().lower()
        user = db.get_user_by_email(em)

        if not user or not check_password_hash(user["password"], password):
            styles.alert("Invalid email or password.", "danger")
        elif not em.endswith(ALLOWED_DOMAIN):
            styles.alert(f"Only {ALLOWED_DOMAIN} accounts are permitted.", "danger")
        elif user["status"] == "pending":
            styles.alert("Your account is pending admin approval.", "warning")
        elif user["status"] == "rejected":
            styles.alert("Your access has been revoked. Contact the administrator.", "danger")
        elif user["status"] == "forced_out":
            styles.alert("You were logged out by an administrator. Contact support.", "danger")
        else:
            db.update_last_login(user["id"])
            st.session_state.user = user
            flash(f"Welcome back, {user['name']}!", "success")
            go("admin" if user["role"] == "admin" else "dashboard")

    if st.button("← Create an account", key="si_to_reg"):
        go("register")

    st.markdown("""
    <div class="notice">
      <span>🔒</span>
      <p>Access restricted to <strong>@hospital.ac.ke</strong> only.
      Unauthorised access attempts are logged and reported.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  PAGE: USER DASHBOARD
# ══════════════════════════════════════════════════════════════
def page_dashboard():
    styles.inject()
    u = st.session_state.user
    if not u:
        go("signin"); return

    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="display:inline-flex;align-items:center;gap:8px;
             background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);
             border-radius:30px;padding:6px 14px;margin-bottom:1.2rem;">
          <span style="color:#b59a5a;font-size:1rem;">✚</span>
          <span style="font-family:'DM Mono',monospace;font-size:.65rem;
                letter-spacing:.1em;text-transform:uppercase;">Hospital.ac.ke</span>
        </div>
        """, unsafe_allow_html=True)
    sidebar_user()

    show_flash()

    # Welcome banner
    first = u["name"].split()[0]
    st.markdown(f"""
    <div class="dash-welcome">
      <div class="dw-inner">
        <div style="display:inline-flex;align-items:center;gap:6px;
             background:rgba(74,222,128,.15);border:1px solid rgba(74,222,128,.3);
             border-radius:20px;padding:4px 12px;margin-bottom:.8rem;">
          <span style="color:#4ade80;font-size:.75rem;">✓</span>
          <span style="font-family:'DM Mono',monospace;font-size:.65rem;
                color:#4ade80;text-transform:uppercase;letter-spacing:.09em;">Access granted</span>
        </div>
        <h2>Clinical BioBERT<br>ICD-11 Portal</h2>
        <p>Your account has been approved, {first}. You now have access to the
        BioBERT-powered ICD-11 medical coding research environment using
        <strong style="color:rgba(255,255,255,.8)">dmis-lab/biobert-base-cased-v1.2</strong>.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Info grid
    col1, col2, col3 = st.columns(3)
    for col, label, value in [
        (col1, "Account Email",  u["email"]),
        (col2, "Last Login",     (u.get("last_login") or "First login")[:16]),
        (col3, "Account Status", "✓ Approved"),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card">
              <div class="ml">{label}</div>
              <div style="font-family:'DM Mono',monospace;font-size:.82rem;
                   color:var(--ink);margin-top:.4rem;word-break:break-all;">{value}</div>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  PAGE: ADMIN PANEL
# ══════════════════════════════════════════════════════════════
def page_admin():
    styles.inject()
    u = st.session_state.user
    if not u or u["role"] != "admin":
        go("signin"); return

    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="display:inline-flex;align-items:center;gap:8px;
             background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);
             border-radius:30px;padding:6px 14px;margin-bottom:1.2rem;">
          <span style="color:#b59a5a;">✚</span>
          <span style="font-family:'DM Mono',monospace;font-size:.65rem;
                letter-spacing:.1em;text-transform:uppercase;">Hospital.ac.ke</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div style="font-family:\'DM Mono\',monospace;font-size:.62rem;color:var(--gold);text-transform:uppercase;letter-spacing:.09em;margin-bottom:1rem;">Administrator</div>', unsafe_allow_html=True)
    sidebar_user()

    show_flash()

    # Header
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
      <div class="eyebrow">Admin Panel</div>
      <div style="font-family:'DM Serif Display',serif;font-size:1.9rem;color:var(--ink);">User Management</div>
      <div style="font-size:.84rem;color:var(--muted);margin-top:.3rem;">
        Approve registrations, manage access, and monitor sessions.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Load users
    users    = db.get_all_non_admin_users()
    pending  = [x for x in users if x["status"] == "pending"]
    approved = [x for x in users if x["status"] == "approved"]
    others   = [x for x in users if x["status"] not in ("pending", "approved")]

    # Metric cards
    col1, col2, col3, col4 = st.columns(4)
    for col, label, num, cls in [
        (col1, "Total Users",     len(users),    ""),
        (col2, "Pending",         len(pending),  "mc-pending"),
        (col3, "Approved",        len(approved), "mc-approved"),
        (col4, "Rejected/Blocked",len(others),   "mc-rejected"),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card {cls}">
              <div class="mn">{num}</div>
              <div class="ml">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Pending ──────────────────────────────────────────────
    st.markdown(f"""
    <div class="section-card">
      <div class="section-head">
        <h3>⏳ Pending Approval</h3>
        <span class="count-badge">{len(pending)}</span>
      </div>
    </div>""", unsafe_allow_html=True)

    if not pending:
        st.info("No pending requests.", icon="✅")
    else:
        for usr in pending:
            with st.container():
                c1, c2, c3, c4, c5 = st.columns([2, 2.5, 1.5, 1, 1])
                c1.markdown(f"**{usr['name']}**")
                c2.markdown(f"`{usr['email']}`")
                c3.markdown(f"<span class='sb sb-pending'>Pending</span>", unsafe_allow_html=True)
                with c4:
                    if st.button("✓ Approve", key=f"apr_{usr['id']}"):
                        db.set_user_status(usr["id"], "approved")
                        flash(f"{usr['name']} approved.", "success")
                        st.rerun()
                with c5:
                    if st.button("✕ Reject", key=f"rej_{usr['id']}"):
                        db.set_user_status(usr["id"], "rejected")
                        flash(f"{usr['name']} rejected.", "warning")
                        st.rerun()
                st.divider()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Approved ─────────────────────────────────────────────
    st.markdown(f"""
    <div class="section-card">
      <div class="section-head">
        <h3>✅ Approved Users</h3>
        <span class="count-badge">{len(approved)}</span>
      </div>
    </div>""", unsafe_allow_html=True)

    if not approved:
        st.info("No approved users yet.")
    else:
        for usr in approved:
            online = bool(usr.get("logged_in"))
            session_badge = (
                "<span class='sb sb-online'>● Online</span>"
                if online else
                "<span class='sb sb-offline'>○ Offline</span>"
            )
            last = (usr.get("last_login") or "—")[:16]

            with st.container():
                c1, c2, c3, c4, c5, c6 = st.columns([2, 2.5, 1.2, 1.5, 1.2, 1.2])
                c1.markdown(f"**{usr['name']}**")
                c2.markdown(f"`{usr['email']}`")
                c3.markdown(session_badge, unsafe_allow_html=True)
                c4.markdown(f"<small style='color:var(--muted)'>{last}</small>", unsafe_allow_html=True)
                with c5:
                    if st.button("⏏ Force Out", key=f"fo_{usr['id']}"):
                        db.set_user_status(usr["id"], "forced_out")
                        flash(f"{usr['name']} has been force-logged out.", "danger")
                        st.rerun()
                with c6:
                    if st.button("✕ Revoke", key=f"rev_{usr['id']}"):
                        db.set_user_status(usr["id"], "rejected")
                        flash(f"{usr['name']}'s access revoked.", "warning")
                        st.rerun()
                st.divider()

    # ── Rejected / Blocked ────────────────────────────────────
    if others:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="section-card">
          <div class="section-head">
            <h3>🚫 Rejected / Blocked</h3>
            <span class="count-badge">{len(others)}</span>
          </div>
        </div>""", unsafe_allow_html=True)

        for usr in others:
            badge_cls = "sb-forced" if usr["status"] == "forced_out" else "sb-rejected"
            badge_txt = "Force Removed" if usr["status"] == "forced_out" else "Rejected"
            with st.container():
                c1, c2, c3, c4 = st.columns([2, 2.5, 1.5, 1.5])
                c1.markdown(f"**{usr['name']}**")
                c2.markdown(f"`{usr['email']}`")
                c3.markdown(f"<span class='sb {badge_cls}'>{badge_txt}</span>", unsafe_allow_html=True)
                with c4:
                    if st.button("↩ Reinstate", key=f"re_{usr['id']}"):
                        db.set_user_status(usr["id"], "approved")
                        flash(f"{usr['name']} reinstated.", "success")
                        st.rerun()
                st.divider()


# ══════════════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════════════
PAGE_MAP = {
    "register":  page_register,
    "signin":    page_signin,
    "dashboard": page_dashboard,
    "admin":     page_admin,
}

# Guard: redirect to signin if not logged in on protected pages
if st.session_state.page in ("dashboard", "admin") and not st.session_state.user:
    st.session_state.page = "signin"

PAGE_MAP[st.session_state.page]()
