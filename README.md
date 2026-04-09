# 🏥 Clinical BioBERT — Auth Portal (Streamlit)

A Streamlit authentication portal for the Clinical BioBERT ICD-11 project.  
Restricts access to `@hospital.ac.ke` emails with an admin approval workflow.

---

## 📁 Project Structure

```
biobert_app/
├── app.py                  # Main Streamlit application (all pages)
├── db.py                   # SQLite database layer
├── styles.py               # Shared CSS & HTML components
├── requirements.txt        # Python dependencies
├── .gitignore
└── .streamlit/
    └── config.toml         # Theme & server settings
```

---

## 🚀 Deploy to Streamlit Cloud (Free) — Step by Step

### Step 1 — Push to GitHub

```bash
# In your terminal
cd biobert_app
git init
git add .
git commit -m "Initial commit — Clinical BioBERT portal"

# Create a new repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### Step 2 — Deploy on Streamlit Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with your GitHub account
3. Click **"New app"**
4. Set:
   - **Repository:** `YOUR_USERNAME/YOUR_REPO`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **"Deploy"** — done! 🎉

Your app will be live at:  
`https://YOUR_USERNAME-YOUR_REPO-app-XXXX.streamlit.app`

---

## 🔐 Default Admin Credentials

| Field    | Value                    |
|----------|--------------------------|
| Email    | `admin@hospital.ac.ke`   |
| Password | `Admin@1234`             |

> ⚠️ Change the admin password in `db.py → init_db()` before deploying.

---

## 👤 User Flow

```
Register (/register)
    ↓  (only @hospital.ac.ke allowed)
Account created → status: PENDING
    ↓
Admin logs in → Admin Panel
    ↓  Approve / Reject / Force Logout
User signs in → Dashboard
```

---

## 🛠 Admin Actions

| Action       | Description                                           |
|--------------|-------------------------------------------------------|
| ✓ Approve    | Unlocks the account — user can now sign in            |
| ✕ Reject     | Blocks with rejection message                         |
| ⏏ Force Out  | Immediately kills session + blocks future login       |
| ↩ Reinstate  | Restores a rejected/blocked user to approved status   |

---

## ⚠️ Important: Database on Streamlit Cloud

Streamlit Cloud uses **ephemeral storage** — the SQLite database resets on each redeploy.

**For persistent storage in production, replace SQLite with:**
- [Supabase](https://supabase.com) (free PostgreSQL)
- [PlanetScale](https://planetscale.com) (free MySQL)
- [MongoDB Atlas](https://www.mongodb.com/atlas) (free NoSQL)

All are free-tier and work seamlessly with Streamlit via `st.secrets`.

---

## 💻 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open: http://localhost:8501
