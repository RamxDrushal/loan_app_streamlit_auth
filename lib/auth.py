import re
import bcrypt
import mysql

from lib.db import get_connection

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def _hash_password(pw: str) -> str:
    return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def _check_password(pw: str, pw_hash: str) -> bool:
    try:
        return bcrypt.checkpw(pw.encode("utf-8"), pw_hash.encode("utf-8"))
    except Exception:
        return False

def _user_exists(conn, email: str) -> bool:
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM users WHERE email=%s", (email.strip().lower(),))
        exists = cur.fetchone() is not None
        return exists
    finally:
        cur.close()

def create_user(name: str, email: str, password: str):
    conn, err = get_connection()
    if err:
        return False, f"Database connection error: {err}"

    name = (name or "").strip()
    email = (email or "").strip().lower()
    if len(name) < 2:
        return False, "Please enter your full name."
    if not EMAIL_REGEX.match(email):
        return False, "Please enter a valid email."
    if len(password or "") < 6:
        return False, "Password must be at least 6 characters."
    if _user_exists(conn, email):
        return False, "Email is already registered."

    pw_hash = _hash_password(password)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users(name, email, password_hash) VALUES (%s, %s, %s)",
            (name, email, pw_hash),
        )
        return True, "Account created successfully!"
    except mysql.connector.Error as err:
        return False, f"Database error: {err}"
    finally:
        cur.close()
        conn.close()

def authenticate(email: str, password: str):
    conn, err = get_connection()
    if err:
        return None, f"Database connection error: {err}"

    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT id, name, email, password_hash, created_at FROM users WHERE email=%s",
            (email.strip().lower(),),
        )
        row = cur.fetchone()
        if not row:
            return None, "No account found with that email."
        if not _check_password(password, row["password_hash"]):
            return None, "Incorrect password."
        row.pop("password_hash", None)
        return row, None
    except mysql.connector.Error as err:
        return None, f"Database error: {err}"
    finally:
        cur.close()
        conn.close()
