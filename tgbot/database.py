import sqlite3
from contextlib import closing
from typing import Optional
from datetime import datetime, timedelta

DB_PATH = "bot.db"


def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn, conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                requests_count INTEGER DEFAULT 0,
                is_premium INTEGER DEFAULT 0,
                premium_until TEXT DEFAULT NULL
            )
        """)
        columns = {
            row[1] for row in conn.execute("PRAGMA table_info(users)").fetchall()
        }
        if "referred_by" not in columns:
            conn.execute(
                "ALTER TABLE users ADD COLUMN referred_by INTEGER DEFAULT NULL"
            )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_users_referred_by "
            "ON users(referred_by)"
        )
        conn.commit()


def get_or_create_user(user_id: int, username: Optional[str]) -> dict:
    with closing(sqlite3.connect(DB_PATH)) as conn, conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        if row:
            return dict(row)
        conn.execute(
            "INSERT INTO users (id, username) VALUES (?, ?)",
            (user_id, username)
        )
        conn.commit()
        return {
            "id": user_id,
            "username": username,
            "requests_count": 0,
            "is_premium": 0,
            "premium_until": None,
            "referred_by": None,
        }


def register_user(
    user_id: int,
    username: Optional[str],
    referrer_id: Optional[int] = None,
    max_referrals: int = 3,
) -> tuple[dict, Optional[int]]:
    """Create a user and atomically credit a valid referral once."""
    with closing(sqlite3.connect(DB_PATH)) as conn, conn:
        conn.row_factory = sqlite3.Row
        conn.execute("BEGIN IMMEDIATE")

        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if row:
            if username != row["username"]:
                conn.execute(
                    "UPDATE users SET username = ? WHERE id = ?",
                    (username, user_id),
                )
                conn.commit()
                row = conn.execute(
                    "SELECT * FROM users WHERE id = ?", (user_id,)
                ).fetchone()
            return dict(row), None

        credited_referrer = None
        if referrer_id and referrer_id != user_id:
            referrer_exists = conn.execute(
                "SELECT 1 FROM users WHERE id = ?", (referrer_id,)
            ).fetchone()
            referral_count = conn.execute(
                "SELECT COUNT(*) FROM users WHERE referred_by = ?",
                (referrer_id,),
            ).fetchone()[0]
            if referrer_exists and referral_count < max_referrals:
                credited_referrer = referrer_id

        conn.execute(
            "INSERT INTO users (id, username, referred_by) VALUES (?, ?, ?)",
            (user_id, username, credited_referrer),
        )
        conn.commit()
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(user), credited_referrer


def get_referral_count(user_id: int) -> int:
    with closing(sqlite3.connect(DB_PATH)) as conn, conn:
        return conn.execute(
            "SELECT COUNT(*) FROM users WHERE referred_by = ?", (user_id,)
        ).fetchone()[0]


def increment_requests(user_id: int):
    with closing(sqlite3.connect(DB_PATH)) as conn, conn:
        conn.execute(
            "UPDATE users SET requests_count = requests_count + 1 WHERE id = ?",
            (user_id,)
        )
        conn.commit()


def set_premium(user_id: int, status: bool = True):
    with closing(sqlite3.connect(DB_PATH)) as conn, conn:
        conn.execute(
            "UPDATE users SET is_premium = ? WHERE id = ?",
            (1 if status else 0, user_id)
        )
        conn.commit()


def check_premium_expired(user_id: int) -> bool:
    user = get_or_create_user(user_id, None)
    if not user["is_premium"] or not user["premium_until"]:
        return False
    try:
        until = datetime.fromisoformat(user["premium_until"])
        if datetime.now() > until:
            set_premium(user_id, False)
            return True
    except (ValueError, TypeError):
        pass
    return False
