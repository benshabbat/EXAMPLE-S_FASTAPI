from fastapi import FastAPI, Request, HTTPException
import json
import os
import uvicorn
from datetime import datetime

app = FastAPI()

# נתיב לקובץ JSON
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
NOTES_FILE = os.path.join(DATA_DIR, "notes.json")
LOG_FILE = os.path.join(DATA_DIR, "activity_log.json")

# יצירת תיקיית data אם לא קיימת
os.makedirs(DATA_DIR, exist_ok=True)


def load_json_file(filepath):
    """טוען קובץ JSON, אם לא קיים מחזיר רשימה ריקה"""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_json_file(filepath, data):
    """שומר נתונים לקובץ JSON"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def log_activity(action, details):
    """רושם פעילות ללוג"""
    logs = load_json_file(LOG_FILE)
    logs.append({
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "details": details
    })
    save_json_file(LOG_FILE, logs)


@app.get("/")
def read_root():
    """דף הבית"""
    return {
        "message": "FastAPI JSON Demo",
        "endpoints": {
            "users": "/users",
            "notes": "/notes",
            "logs": "/logs",
            "backup": "/backup",
            "export": "/export"
        }
    }


# ==================== USERS ====================

@app.get("/users")
def get_users():
    """GET - קבלת כל המשתמשים מקובץ JSON"""
    users = load_json_file(USERS_FILE)
    return {"count": len(users), "users": users}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    """GET - קבלת משתמש ספציפי"""
    users = load_json_file(USERS_FILE)
    user = next((u for u in users if u.get("id") == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users")
async def create_user(request: Request):
    """POST - יצירת משתמש חדש ושמירה ל-JSON"""
    body = await request.json()
    users = load_json_file(USERS_FILE)
    
    # יצירת ID חדש
    new_id = max([u.get("id", 0) for u in users], default=0) + 1
    
    new_user = {
        "id": new_id,
        "name": body.get("name"),
        "email": body.get("email"),
        "age": body.get("age"),
        "created_at": datetime.now().isoformat()
    }
    
    users.append(new_user)
    save_json_file(USERS_FILE, users)
    log_activity("CREATE_USER", f"Created user {new_id}")
    
    return {"message": "User created", "user": new_user}


@app.put("/users/{user_id}")
async def update_user(user_id: int, request: Request):
    """PUT - עדכון משתמש ושמירה"""
    body = await request.json()
    users = load_json_file(USERS_FILE)
    
    user_index = next((i for i, u in enumerate(users) if u.get("id") == user_id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    users[user_index] = {
        "id": user_id,
        "name": body.get("name"),
        "email": body.get("email"),
        "age": body.get("age"),
        "updated_at": datetime.now().isoformat()
    }
    
    save_json_file(USERS_FILE, users)
    log_activity("UPDATE_USER", f"Updated user {user_id}")
    
    return {"message": "User updated", "user": users[user_index]}


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """DELETE - מחיקת משתמש"""
    users = load_json_file(USERS_FILE)
    users = [u for u in users if u.get("id") != user_id]
    save_json_file(USERS_FILE, users)
    log_activity("DELETE_USER", f"Deleted user {user_id}")
    
    return {"message": f"User {user_id} deleted"}


# ==================== NOTES ====================

@app.get("/notes")
def get_notes():
    """GET - קבלת כל ההערות"""
    notes = load_json_file(NOTES_FILE)
    return {"count": len(notes), "notes": notes}


@app.post("/notes")
async def create_note(request: Request):
    """POST - יצירת הערה חדשה"""
    body = await request.json()
    notes = load_json_file(NOTES_FILE)
    
    new_id = max([n.get("id", 0) for n in notes], default=0) + 1
    
    new_note = {
        "id": new_id,
        "title": body.get("title"),
        "content": body.get("content"),
        "tags": body.get("tags", []),
        "created_at": datetime.now().isoformat()
    }
    
    notes.append(new_note)
    save_json_file(NOTES_FILE, notes)
    log_activity("CREATE_NOTE", f"Created note {new_id}")
    
    return {"message": "Note created", "note": new_note}


@app.patch("/notes/{note_id}")
async def update_note(note_id: int, request: Request):
    """PATCH - עדכון חלקי של הערה"""
    body = await request.json()
    notes = load_json_file(NOTES_FILE)
    
    note = next((n for n in notes if n.get("id") == note_id), None)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # עדכון רק השדות שנשלחו
    if "title" in body:
        note["title"] = body["title"]
    if "content" in body:
        note["content"] = body["content"]
    if "tags" in body:
        note["tags"] = body["tags"]
    
    note["updated_at"] = datetime.now().isoformat()
    
    save_json_file(NOTES_FILE, notes)
    log_activity("UPDATE_NOTE", f"Updated note {note_id}")
    
    return {"message": "Note updated", "note": note}


# ==================== LOGS ====================

@app.get("/logs")
def get_logs():
    """GET - קבלת כל הלוגים"""
    logs = load_json_file(LOG_FILE)
    return {"count": len(logs), "logs": logs}


@app.delete("/logs")
def clear_logs():
    """DELETE - ניקוי כל הלוגים"""
    save_json_file(LOG_FILE, [])
    return {"message": "Logs cleared"}


# ==================== BACKUP & EXPORT ====================

@app.post("/backup")
def create_backup():
    """POST - יצירת גיבוי של כל הנתונים"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(DATA_DIR, f"backup_{timestamp}.json")
    
    backup_data = {
        "timestamp": datetime.now().isoformat(),
        "users": load_json_file(USERS_FILE),
        "notes": load_json_file(NOTES_FILE),
        "logs": load_json_file(LOG_FILE)
    }
    
    save_json_file(backup_file, backup_data)
    
    return {
        "message": "Backup created",
        "file": backup_file,
        "data": backup_data
    }


@app.get("/export")
def export_all_data():
    """GET - ייצוא כל הנתונים בפורמט JSON אחד"""
    return {
        "exported_at": datetime.now().isoformat(),
        "users": load_json_file(USERS_FILE),
        "notes": load_json_file(NOTES_FILE),
        "logs": load_json_file(LOG_FILE)
    }


@app.post("/import")
async def import_data(request: Request):
    """POST - ייבוא נתונים מ-JSON"""
    body = await request.json()
    
    if "users" in body:
        save_json_file(USERS_FILE, body["users"])
    if "notes" in body:
        save_json_file(NOTES_FILE, body["notes"])
    
    log_activity("IMPORT_DATA", "Imported data from JSON")
    
    return {"message": "Data imported successfully"}


@app.delete("/reset")
def reset_all_data():
    """DELETE - מחיקת כל הנתונים"""
    save_json_file(USERS_FILE, [])
    save_json_file(NOTES_FILE, [])
    save_json_file(LOG_FILE, [])
    
    return {"message": "All data has been reset"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
