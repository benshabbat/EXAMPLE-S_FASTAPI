# ייבוא הספריות הנדרשות
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# יצירת אפליקציית FastAPI
app = FastAPI(
    title="Todo API",
    description="API פשוטה לניהול משימות",
    version="1.0.0"
)

# === מודלים (Models) ===

class TodoBase(BaseModel):
    """
    מודל בסיסי למשימה
    כולל את השדות הבסיסיים שנדרשים ליצירת משימה
    """
    title: str  # כותרת המשימה (חובה)
    description: Optional[str] = None  # תיאור המשימה (אופציונלי)
    completed: bool = False  # האם המשימה הושלמה (ברירת מחדל: לא)

class TodoCreate(TodoBase):
    """
    מודל ליצירת משימה חדשה
    יורש מ-TodoBase ולא מוסיף שדות נוספים
    """
    pass

class TodoUpdate(BaseModel):
    """
    מודל לעדכון משימה קיימת
    כל השדות הם אופציונליים כך שניתן לעדכן רק חלק מהשדות
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(TodoBase):
    """
    מודל מלא של משימה כולל ID ותאריך יצירה
    זה מה שמוחזר למשתמש
    """
    id: int
    created_at: str

    class Config:
        # מאפשר המרה אוטומטית מ-dictionary
        from_attributes = True

# === אחסון זמני בזיכרון ===
# במקום מסד נתונים, נשתמש ברשימה פשוטה
# שימו לב: הנתונים יאבדו כשהשרת יכבה
todos_db: List[dict] = []
# מונה למתן ID ייחודי לכל משימה
todo_counter = 1

# === נקודות קצה (Endpoints) ===

@app.get("/", tags=["ראשי"])
async def root():
    """
    נקודת קצה ראשית - מחזירה הודעת ברוכים הבאים
    """
    return {
        "message": "ברוכים הבאים ל-Todo API!",
        "docs": "/docs - לתיעוד אינטראקטיבי"
    }

@app.get("/todos", response_model=List[Todo], tags=["משימות"])
async def get_all_todos(completed: Optional[bool] = None):
    """
    מחזיר את כל המשימות
    
    פרמטרים:
    - completed (אופציונלי): סינון לפי סטטוס השלמה
      - True: רק משימות שהושלמו
      - False: רק משימות שלא הושלמו
      - None: כל המשימות
    """
    if completed is None:
        # מחזיר את כל המשימות
        return todos_db
    
    # מסנן משימות לפי סטטוס
    return [todo for todo in todos_db if todo["completed"] == completed]

@app.get("/todos/{todo_id}", response_model=Todo, tags=["משימות"])
async def get_todo(todo_id: int):
    """
    מחזיר משימה ספציפית לפי ID
    
    פרמטרים:
    - todo_id: מספר המזהה של המשימה
    
    זורק שגיאה 404 אם המשימה לא נמצאה
    """
    # חיפוש המשימה ברשימה
    for todo in todos_db:
        if todo["id"] == todo_id:
            return todo
    
    # אם לא נמצא - זריקת שגיאה
    raise HTTPException(
        status_code=404,
        detail=f"משימה עם ID {todo_id} לא נמצאה"
    )

@app.post("/todos", response_model=Todo, status_code=201, tags=["משימות"])
async def create_todo(todo: TodoCreate):
    """
    יצירת משימה חדשה
    
    Body:
    - title: כותרת המשימה (חובה)
    - description: תיאור המשימה (אופציונלי)
    - completed: האם המשימה הושלמה (ברירת מחדל: False)
    
    מחזיר את המשימה שנוצרה עם ID ותאריך יצירה
    """
    global todo_counter
    
    # יצירת אובייקט משימה חדש
    new_todo = {
        "id": todo_counter,
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # הוספת המשימה לרשימה
    todos_db.append(new_todo)
    
    # הגדלת המונה למשימה הבאה
    todo_counter += 1
    
    return new_todo

@app.put("/todos/{todo_id}", response_model=Todo, tags=["משימות"])
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    """
    עדכון משימה קיימת
    
    פרמטרים:
    - todo_id: מספר המזהה של המשימה לעדכון
    
    Body (כל השדות אופציונליים):
    - title: כותרת חדשה
    - description: תיאור חדש
    - completed: סטטוס השלמה חדש
    
    מעדכן רק את השדות שנשלחו
    """
    # חיפוש המשימה
    for todo in todos_db:
        if todo["id"] == todo_id:
            # עדכון רק השדות שנשלחו
            if todo_update.title is not None:
                todo["title"] = todo_update.title
            if todo_update.description is not None:
                todo["description"] = todo_update.description
            if todo_update.completed is not None:
                todo["completed"] = todo_update.completed
            
            return todo
    
    # אם לא נמצא - זריקת שגיאה
    raise HTTPException(
        status_code=404,
        detail=f"משימה עם ID {todo_id} לא נמצאה"
    )

@app.delete("/todos/{todo_id}", tags=["משימות"])
async def delete_todo(todo_id: int):
    """
    מחיקת משימה
    
    פרמטרים:
    - todo_id: מספר המזהה של המשימה למחיקה
    """
    global todos_db
    
    # חיפוש ומחיקת המשימה
    for i, todo in enumerate(todos_db):
        if todo["id"] == todo_id:
            deleted_todo = todos_db.pop(i)
            return {
                "message": "המשימה נמחקה בהצלחה",
                "deleted_todo": deleted_todo
            }
    
    # אם לא נמצא - זריקת שגיאה
    raise HTTPException(
        status_code=404,
        detail=f"משימה עם ID {todo_id} לא נמצאה"
    )

@app.patch("/todos/{todo_id}/toggle", response_model=Todo, tags=["משימות"])
async def toggle_todo_completion(todo_id: int):
    """
    הפיכת סטטוס ההשלמה של המשימה (completed ↔ not completed)
    
    פרמטרים:
    - todo_id: מספר המזהה של המשימה
    """
    for todo in todos_db:
        if todo["id"] == todo_id:
            # הפיכת הסטטוס
            todo["completed"] = not todo["completed"]
            return todo
    
    raise HTTPException(
        status_code=404,
        detail=f"משימה עם ID {todo_id} לא נמצאה"
    )

@app.delete("/todos", tags=["משימות"])
async def delete_all_todos():
    """
    מחיקת כל המשימות
    זהירות: פעולה זו בלתי הפיכה!
    """
    global todos_db, todo_counter
    
    deleted_count = len(todos_db)
    todos_db = []
    todo_counter = 1
    
    return {
        "message": f"{deleted_count} משימות נמחקו בהצלחה",
        "remaining_todos": 0
    }

# הרצת השרת (רק אם הקובץ מורץ ישירות)
if __name__ == "__main__":
    import uvicorn
    print("🚀 מתחיל את שרת Todo API...")
    print("📖 תיעוד זמין בכתובת: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)
