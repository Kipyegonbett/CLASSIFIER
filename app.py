"""
app.py — Clinical BioBERT Auth Portal (Streamlit)
FIXED VERSION: Stable role-based routing
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
    "user": None,
    "flash": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Helpers ────────────────────────────────────────────────────
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
    st.rerun()

def sidebar_user():
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

        if st.button("⏏ Sign out"):
            logout()

# ══════════════════════════════════════════════════════════════
# REGISTER
# ══════════════════════════════════════════════════════════════
def page_register():
    styles.inject()
    styles.banner(
        "Join Clinical BioBERT Portal",
        "Create your hospital account (requires admin approval)."
    )

    show_flash()

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if not email.endswith(ALLOWED_DOMAIN):
            styles.alert("Use hospital email.", "danger")
        elif password != confirm:
            styles.alert("Passwords do not match.", "danger")
        else:
            ok, err = db.create_user(
                name,
                email.lower(),
                generate_password_hash(password)
            )
            if ok:
                flash("Account created. Wait for approval.", "success")
                st.rerun()
            else:
                styles.alert(err, "danger")

# ══════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════
def page_signin():
    styles.inject()
    styles.banner("Clinical BioBERT", "Secure Sign In")

    show_flash()

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = db.get_user_by_email(email.lower())

        if not user or not check_password_hash(user["password"], password):
            styles.alert("Invalid credentials", "danger")

        elif user["status"] != "approved":
            styles.alert(f"Account status: {user['status']}", "warning")

        else:
            db.update_last_login(user["id"])
            st.session_state.user = user
            flash(f"Welcome {user['name']}", "success")
            st.rerun()

# ══════════════════════════════════════════════════════════════
# USER DASHBOARD
# ══════════════════════════════════════════════════════════════
def page_dashboard():
    styles.inject()
    u = st.session_state.user

    sidebar_user()
    show_flash()

    st.title("User Dashboard")
    st.write(f"Welcome {u['name']}")
    st.write(f"Email: {u['email']}")

# ══════════════════════════════════════════════════════════════
# ADMIN DASHBOARD
# ══════════════════════════════════════════════════════════════
def page_admin():
    styles.inject()
    u = st.session_state.user

    sidebar_user()
    show_flash()

    st.title("Admin Panel")

    users = db.get_all_non_admin_users()

    for usr in users:
        st.write(f"{usr['name']} — {usr['status']}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"Approve {usr['id']}"):
                db.set_user_status(usr["id"], "approved")
                st.rerun()

        with col2:
            if st.button(f"Reject {usr['id']}"):
                db.set_user_status(usr["id"], "rejected")
                st.rerun()

# ══════════════════════════════════════════════════════════════
# ROUTER (FIXED)
# ══════════════════════════════════════════════════════════════

user = st.session_state.get("user")

if not user:
    page = st.sidebar.radio("Navigate", ["Sign In", "Register"])

    if page == "Register":
        page_register()
    else:
        page_signin()

else:
    if user["role"] == "admin":
        page_admin()
    else:
        page_dashboard()
