import os

import bcrypt
import mariadb
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}


def get_connection():
    return mariadb.connect(**DB_CONFIG)


def create_account(username: str, password: str, email: str) -> bool:
    #create account. returns true if successful, false if duplicate email/username or otherwise
    
    #bcrypt encryption
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    hashed_str = hashed.decode("utf-8")

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO login (user, pass, email) VALUES (%s, %s, %s)",
            (username, hashed_str, email),
        )
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


def verify_login(username: str, password: str) -> bool:
    # checks user & passward in DB. true if valid, false otherwise
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT pass FROM login WHERE user = %s",
            (username,),
        )
        result = cursor.fetchone()
        cursor.close()

        if result is None:
            return False

        stored_hash = result[0].encode("utf-8")
        password_bytes = password.encode("utf-8")

        return bcrypt.checkpw(password_bytes, stored_hash)

    except mariadb.Error as e:
        print(f"Error verifying login: {e}")
        return False

    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    # sign up
    success = create_account("jdoe", "correct-horse-battery-staple", "jdoe@example.com")
    print("Account created:", success)

    # login
    if verify_login("jdoe", "correct-horse-battery-staple"):
        print("Login successful!")
    else:
        print("Login failed.")
