import json
import os
import pymysql

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "canvas_ai"),
        port=int(os.getenv("DB_PORT", "4000")),
        ssl={"ca": os.getenv("DB_SSL_CA")} if os.getenv("DB_SSL_CA") else None,
        charset="utf8mb4",
    )

def create_session(account_id: int, title: str) -> int:
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO session (account_id, session_title) VALUES (%s, %s)",
                (account_id, title),
            )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def session_belongs_to(session_id: int, account_id: int) -> bool:
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM session WHERE session_id = %s AND account_id = %s",
                (session_id, account_id),
            )
            return cursor.fetchone() is not None
    finally:
        conn.close()

def save_chat(session_id: int, user_message: str, ai_response: str, model: str | None = None) -> int:
    message_json = {"role": "user", "content": user_message}
    response_json = {"role": "assistant", "content": ai_response, "model": model}

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO chat (session_id, message, response) VALUES (%s, %s, %s)",
                (session_id, json.dumps(message_json), json.dumps(response_json)),
            )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def get_chats(session_id: int) -> list[dict]:
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(
                "SELECT chat_id, message, response, created_at FROM chat "
                "WHERE session_id = %s ORDER BY created_at, chat_id",
                (session_id,),
            )
            rows = cursor.fetchall()
    finally:
        conn.close()

    for row in rows:
        row["message"] = json.loads(row["message"])
        row["response"] = json.loads(row["response"]) if row["response"] else None
    return rows

def get_content(stored: str | None) -> str:
    if not stored:
        return ""

    value = json.loads(stored)
    if isinstance(value, dict):
        return str(value.get("content", ""))
    
    return value if isinstance(value, str) else json.dumps(value)

def get_sessions(account_id: int) -> list[dict]:
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(
                "SELECT session_id, session_title, created_at FROM session "
                "WHERE account_id = %s ORDER BY created_at DESC, session_id DESC",
                (account_id,),
            )
            sessions = list(cursor.fetchall())

            cursor.execute(
                "SELECT chat.chat_id, chat.session_id, chat.message, chat.response, chat.created_at "
                "FROM chat JOIN session ON chat.session_id = session.session_id "
                "WHERE session.account_id = %s ORDER BY chat.created_at, chat.chat_id",
                (account_id,),
            )
            chats = cursor.fetchall()
    finally:
        conn.close()

    chats_by_session = {session["session_id"]: [] for session in sessions}
    for chat in chats:
        chats_by_session[chat["session_id"]].append({
            "chat_id": chat["chat_id"],
            "message": get_content(chat["message"]),
            "response": get_content(chat["response"]),
            "created_at": chat["created_at"],
        })

    for session in sessions:
        session["chats"] = chats_by_session[session["session_id"]]
    
    return sessions
