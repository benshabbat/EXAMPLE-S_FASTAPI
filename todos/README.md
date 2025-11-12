# 📝 Todo API - FastAPI

אפליקציית ניהול משימות (Todos) פשוטה ומלאה עם FastAPI.

## 🎯 תכונות

- ✅ יצירת משימות חדשות
- 📋 צפייה בכל המשימות
- 🔍 חיפוש משימה ספציפית
- ✏️ עדכון משימות קיימות
- 🔄 הפיכת סטטוס השלמה
- 🗑️ מחיקת משימות
- 🔎 סינון משימות לפי סטטוס

## 🚀 התקנה והרצה

### 1. התקנת התלויות

```bash
pip install -r requirements.txt
```

### 2. הרצת השרת

```bash
python main.py
```

או:

```bash
uvicorn main:app --reload
```

השרת יעלה בכתובת: `http://127.0.0.1:8000`

### 3. צפייה בתיעוד

פתח בדפדפן: `http://127.0.0.1:8000/docs`

## 📚 API Endpoints

### 1. קבלת כל המשימות
```
GET /todos
```
**פרמטרים אופציונליים:**
- `completed` - סינון לפי סטטוס (true/false)

**דוגמה:**
```bash
curl http://127.0.0.1:8000/todos
curl http://127.0.0.1:8000/todos?completed=true
```

### 2. קבלת משימה ספציפית
```
GET /todos/{todo_id}
```

**דוגמה:**
```bash
curl http://127.0.0.1:8000/todos/1
```

### 3. יצירת משימה חדשה
```
POST /todos
```

**Body:**
```json
{
  "title": "ללמוד FastAPI",
  "description": "לסיים את המדריך",
  "completed": false
}
```

**דוגמה:**
```bash
curl -X POST http://127.0.0.1:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "ללמוד FastAPI", "description": "לסיים את המדריך"}'
```

### 4. עדכון משימה
```
PUT /todos/{todo_id}
```

**Body (כל השדות אופציונליים):**
```json
{
  "title": "ללמוד FastAPI - מתקדם",
  "completed": true
}
```

**דוגמה:**
```bash
curl -X PUT http://127.0.0.1:8000/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### 5. הפיכת סטטוס השלמה
```
PATCH /todos/{todo_id}/toggle
```

**דוגמה:**
```bash
curl -X PATCH http://127.0.0.1:8000/todos/1/toggle
```

### 6. מחיקת משימה
```
DELETE /todos/{todo_id}
```

**דוגמה:**
```bash
curl -X DELETE http://127.0.0.1:8000/todos/1
```

### 7. מחיקת כל המשימות
```
DELETE /todos
```

**דוגמה:**
```bash
curl -X DELETE http://127.0.0.1:8000/todos
```

## 🏗️ מבנה הקוד

### מודלים (Pydantic Models)

1. **TodoBase** - מודל בסיסי עם השדות הבסיסיים
2. **TodoCreate** - למשימה חדשה (יורש מ-TodoBase)
3. **TodoUpdate** - לעדכון משימה (כל השדות אופציונליים)
4. **Todo** - מודל מלא כולל ID ותאריך יצירה

### אחסון נתונים

הנתונים נשמרים בזיכרון (list) - **יאבדו כשהשרת כבה!**

לייצור, מומלץ להשתמש במסד נתונים כמו:
- SQLite (פשוט ומקומי)
- PostgreSQL (מקצועי)
- MongoDB (NoSQL)

## 🎓 מה למדנו?

1. **FastAPI Basics** - יצירת אפליקציה בסיסית
2. **Pydantic Models** - ולידציה אוטומטית של נתונים
3. **HTTP Methods**:
   - GET - קבלת נתונים
   - POST - יצירת משימה
   - PUT - עדכון מלא
   - PATCH - עדכון חלקי
   - DELETE - מחיקה
4. **Path Parameters** - `{todo_id}`
5. **Query Parameters** - `?completed=true`
6. **Request Body** - קבלת JSON מהמשתמש
7. **Response Models** - הגדרת מבנה התשובה
8. **Status Codes** - 201 ליצירה, 404 לא נמצא
9. **Exception Handling** - HTTPException לשגיאות

## 💡 שיפורים אפשריים

- [ ] הוספת מסד נתונים (SQLite/PostgreSQL)
- [ ] הוספת אימות משתמשים (JWT)
- [ ] הוספת תאריכי יעד למשימות
- [ ] הוספת קטגוריות
- [ ] הוספת עדיפויות (Priority)
- [ ] הוספת חיפוש טקסט חופשי
- [ ] הוספת מיון (Sorting)
- [ ] הוספת Pagination

## 🧪 בדיקה ידנית

אחרי הרצת השרת, פתח את http://127.0.0.1:8000/docs ותוכל:
1. לראות את כל ה-endpoints
2. לבדוק כל endpoint ישירות מהדפדפן
3. לראות את המבנה המלא של כל request/response

זה ממשק אינטראקטיבי מעולה לבדיקות!

---

**Enjoy coding! 🎉**
