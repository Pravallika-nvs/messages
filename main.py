from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

conn = sqlite3.connect("messages.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    created_at TEXT NOT NULL
)
""")

conn.commit()
conn.close()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.post("/submit")
def submit(request: Request, message: str = Form(...)):
    message = message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )
    
    if len(message) > 700:
        raise HTTPException(
            status_code=400,
            detail="Message too long"
        )
    
    conn = sqlite3.connect("messages.db")

    cursor = conn.cursor()

    current_time = datetime.now(
    ZoneInfo("Asia/Kolkata")
    ).strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
    """
    INSERT INTO messages(message, created_at)
    VALUES (?, ?)
    """,
    (message, current_time)
    )

    conn.commit()
    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="success.html"
    )

@app.get("/messages")
def view_messages(
    request: Request,
    password: str
):

    if password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    conn = sqlite3.connect("messages.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM messages ORDER BY id DESC"
    )

    messages = cursor.fetchall()

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="messages.html",
        context={"messages": messages}
    )

@app.get("/delete/{message_id}")
def delete_message(
    message_id: int,
    password: str
):

    conn = sqlite3.connect("messages.db")

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM messages WHERE id = ?",
        (message_id,)
    )

    conn.commit()
    conn.close()

    return {"status": "Deleted"}