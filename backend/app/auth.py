import hashlib
import hmac
import os
import secrets
import time
import bcrypt
import mariadb

from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

# MariaDB Cloud needs the requires the ssl file to connect to a database
if os.getenv("DB_SSL", "true").lower() == "true":
    DB_CONFIG["ssl"] = True
    if os.getenv("DB_SSL_CA"):
        DB_CONFIG["ssl_ca"] = os.getenv("DB_SSL_CA")

# either pull secret from .env to sign login tokens, or generate a new one
AUTH_SECRET = os.getenv("AUTH_SECRET") or secrets.token_hex(32)
TOKEN_LIFETIME_SECONDS = 7 * 24 * 60 * 60


class UsernameTakenError(Exception):
    pass


def get_connection():
    return mariadb.connect(**DB_CONFIG)


def create_account(username: str, password: str) -> int:
    # creates an account and returns its new account_id
    # raises UsernameTakenError if the username already exists
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO login (username, password_hash) VALUES (%s, %s)",
            (username, password_hash),
        )
        account_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        return account_id

    except mariadb.IntegrityError as e:
        # 1062 = duplicate key on the unique username index
        if e.errno == 1062:
            raise UsernameTakenError(username) from e
        raise

    finally:
        if conn is not None:
            conn.close()


def verify_login(username: str, password: str) -> tuple[int, str] | None:
    # checks the username/password
    # returns (account_id, username) if correct, None otherwise
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT account_id, username, password_hash FROM login WHERE username = %s",
            (username,),
        )
        row = cursor.fetchone()
        cursor.close()
    finally:
        if conn is not None:
            conn.close()

    if row is None or row[2] is None:
        return None

    account_id, stored_username, password_hash = row
    if not bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8")):
        return None

    return account_id, stored_username


def sign(payload: str) -> str:
    return hmac.new(AUTH_SECRET.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()


def create_token(account_id: int) -> str:
    # token format: "<account_id>.<expiry unix time>.<signature>"
    payload = f"{account_id}.{int(time.time()) + TOKEN_LIFETIME_SECONDS}"
    return f"{payload}.{sign(payload)}"


def verify_token(token: str) -> int | None:
    # returns the account_id the token was issued for, or None if it is invalid/expired
    try:
        account_id, expires, signature = token.split(".")
        if not hmac.compare_digest(signature, sign(f"{account_id}.{expires}")):
            return None
        if int(expires) < time.time():
            return None
        return int(account_id)
    except ValueError:
        return None
