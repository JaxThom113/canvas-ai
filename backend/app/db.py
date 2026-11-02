import json
from typing import Any

from app.auth import get_connection


def insert_login(account_id: int) -> None:
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO login (account_id) VALUES (%s)", (account_id,))
        conn.commit()
        cursor.close()
    finally:
        if conn is not None:
            conn.close()


def insert_session(account_id: int, session_title: str, session_id: int | None = None) -> int:
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if session_id is None:
            cursor.execute(
                "INSERT INTO session (account_id, session_title) VALUES (%s, %s)",
                (account_id, session_title),
            )
            new_id = cursor.lastrowid
        else:
            cursor.execute(
                "INSERT INTO session (session_id, account_id, session_title) VALUES (%s, %s, %s)",
                (session_id, account_id, session_title),
            )
            new_id = session_id
        conn.commit()
        cursor.close()
        return new_id
    finally:
        if conn is not None:
            conn.close()


def insert_chat(session_id: int, message: Any, response: Any | None, chat_id: int | None = None) -> int:
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        message_json = json.dumps(message)
        response_json = json.dumps(response) if response is not None else None
        if chat_id is None:
            cursor.execute(
                "INSERT INTO chat (session_id, message, response) VALUES (%s, %s, %s)",
                (session_id, message_json, response_json),
            )
            new_id = cursor.lastrowid
        else:
            cursor.execute(
                "INSERT INTO chat (chat_id, session_id, message, response) VALUES (%s, %s, %s, %s)",
                (chat_id, session_id, message_json, response_json),
            )
            new_id = chat_id
        conn.commit()
        cursor.close()
        return new_id
    finally:
        if conn is not None:
            conn.close()
