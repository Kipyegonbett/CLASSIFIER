"""
db.py — SQLite database layer for Clinical BioBERT Auth Portal
"""

import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), "biobert.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            email       TEXT    NOT NULL UNIQUE,
            password    TEXT    NOT NULL,
            role        TEXT    NOT NULL DEFAULT 'user',
            status      TEXT    NOT NULL DEFAULT 'pending',
            created_at  TEXT    NOT NULL,
            last_login  TEXT
        );

        CREATE TABLE IF NOT EXISTS sessions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            logged_in   INTEGER NOT NULL DEFAULT 1,
            login_at    TEXT,
            logout_at   TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    """)

    # Seed default admin
    cur = conn.execute("SELECT id FROM users WHERE role='admin' LIMIT 1")
    if not cur.fetchone():
        conn.execute("""
            INSERT INTO users (name, email, password, role, status, created_at)
            VALUES (?,?,?,?,?,?)
        """, (
            "System Admin",
            "admin@hospital.ac.ke",
            generate_password_hash("Admin@1234"),
            "admin", "approved",
            datetime.now().isoformat(timespec="seconds"),
        ))
    conn.commit()
    conn.close()


# ── User queries ────────────────────────────────────────────────

def get_user_by_email(email: str):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(uid: int):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    conn.close()
    return dict(row) if row else None


def create_user(name, email, hashed_pw):
    conn = get_conn()
    try:
        conn.execute("""
            INSERT INTO users (name, email, password, role, status, created_at)
            VALUES (?,?,?,?,?,?)
        """, (name, email, hashed_pw, "user", "pending",
              datetime.now().isoformat(timespec="seconds")))
        conn.commit()
        return True, None
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."
    finally:
        conn.close()


def update_last_login(uid: int):
    conn = get_conn()
    now = datetime.now().isoformat(timespec="seconds")
    conn.execute("UPDATE users SET last_login=? WHERE id=?", (now, uid))
    conn.execute("INSERT INTO sessions (user_id, logged_in, login_at) VALUES (?,1,?)",
                 (uid, now))
    conn.commit()
    conn.close()


def record_logout(uid: int):
    conn = get_conn()
    now = datetime.now().isoformat(timespec="seconds")
    conn.execute("""UPDATE sessions SET logged_in=0, logout_at=?
                    WHERE user_id=? AND logged_in=1""", (now, uid))
    conn.commit()
    conn.close()


# ── Admin queries ───────────────────────────────────────────────

def get_all_non_admin_users():
    conn = get_conn()
    rows = conn.execute("""
        SELECT u.*,
               s.logged_in,
               s.login_at
        FROM   users u
        LEFT JOIN sessions s
               ON s.user_id = u.id
              AND s.id = (SELECT MAX(id) FROM sessions WHERE user_id = u.id)
        WHERE  u.role != 'admin'
        ORDER  BY u.created_at DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def set_user_status(uid: int, status: str):
    conn = get_conn()
    conn.execute("UPDATE users SET status=? WHERE id=?", (status, uid))
    if status == "forced_out":
        now = datetime.now().isoformat(timespec="seconds")
        conn.execute("""UPDATE sessions SET logged_in=0, logout_at=?
                        WHERE user_id=? AND logged_in=1""", (now, uid))
    conn.commit()
    conn.close()
