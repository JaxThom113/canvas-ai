import os

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

# MariaDB Cloud requires TLS. DB_SSL_CA (optional) points at the CA bundle
# downloaded from the cloud console; without it the server cert is verified
# against the system trust store.
if os.getenv("DB_SSL", "true").lower() == "true":
    DB_CONFIG["ssl"] = True
    if os.getenv("DB_SSL_CA"):
        DB_CONFIG["ssl_ca"] = os.getenv("DB_SSL_CA")


def get_connection():
    return mariadb.connect(**DB_CONFIG)


def create_account(account_id: int) -> bool:
    # create account. returns true if successful, false if duplicate account_id or otherwise
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO login (account_id) VALUES (%s)", (account_id,))
        conn.commit()
        cursor.close()
        return True

    except mariadb.Error as e:
        # duplicate error
        print(f"Error creating account: {e}")
        return False

    finally:
        if conn is not None:
            conn.close()


def verify_login(account_id: int) -> bool:
    # checks that the account_id exists in the DB. true if found, false otherwise
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM login WHERE account_id = %s", (account_id,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    except mariadb.Error as e:
        print(f"Error verifying login: {e}")
        return False

    finally:
        if conn is not None:
            conn.close()


def login(account_id: int) -> bool:
    # first login for this account creates its row
    if verify_login(account_id):
        return True
    return create_account(account_id)


if __name__ == "__main__":
    # sign up
    success = create_account(123456)
    print("Account created:", success)

    # login
    if verify_login(123456):
        print("Login successful!")
    else:
        print("Login failed.")
