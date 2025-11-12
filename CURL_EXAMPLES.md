# דוגמאות CURL לכל ה-APIs

## 📌 הערות חשובות
- כל הדוגמאות מניחות שהשרת רץ על `http://localhost:8000`
- שים לב ליציאה (port) הנכונה לכל API אם הם רצים על יציאות שונות
- עבור Windows PowerShell, השתמש ב-`"` במקום `'` לציטוטים

---

## 🔧 Example Standard API (`exampleStandart/main.py`)

### 1. GET - דף בית
```bash
curl http://localhost:8000/
```

### 2. GET - קבלת פריט לפי ID
```bash
curl http://localhost:8000/items/5
```

### 3. GET - חיפוש עם query parameters
```bash
curl "http://localhost:8000/search?q=phone&skip=0&limit=10"
```

### 4. GET - פריטים של משתמש
```bash
curl "http://localhost:8000/users/1/items?skip=0&limit=5"
```

### 5. POST - יצירת פריט חדש
```bash
curl -X POST http://localhost:8000/items ^
  -H "Content-Type: application/json" ^
  -d "{\"name\": \"Laptop\", \"description\": \"Gaming laptop\", \"price\": 1200.0, \"tax\": 120.0}"
```

**גרסת PowerShell:**
```powershell
curl -Uri http://localhost:8000/items -Method POST -ContentType "application/json" -Body '{"name": "Laptop", "description": "Gaming laptop", "price": 1200.0, "tax": 120.0}'
```

### 6. PUT - עדכון פריט קיים
```bash
curl -X PUT http://localhost:8000/items/5 ^
  -H "Content-Type: application/json" ^
  -d "{\"name\": \"Updated Laptop\", \"price\": 1500.0}"
```

**גרסת PowerShell:**
```powershell
curl -Uri http://localhost:8000/items/5 -Method PUT -ContentType "application/json" -Body '{"name": "Updated Laptop", "price": 1500.0}'
```

---

## 📝 Strings API (`strings/main.py`)

### 1. GET - הפיכת מחרוזת
```bash
curl "http://localhost:8000/reverse?text=hello"
```

### 2. GET - המרה לאותיות גדולות (path parameter)
```bash
curl http://localhost:8000/uppercase/hello
```

### 3. POST - הסרת תנועות
```bash
curl -X POST "http://localhost:8000/remove-vowels?s=hello"
```

**גרסת PowerShell:**
```powershell
curl -Uri "http://localhost:8000/remove-vowels?s=hello" -Method POST
```

### 4. POST - הסרת כל תו שלישי
```bash
curl -X POST "http://localhost:8000/remove-every-third?s=abcdefgh"
```

**גרסת PowerShell:**
```powershell
curl -Uri "http://localhost:8000/remove-every-third?s=abcdefgh" -Method POST
```

### 5. GET - ספירת אותיות
```bash
curl "http://localhost:8000/letter-counts/?text=hello"
```

---

## ✅ Todos API (`todos/main.py`)

### 1. GET - דף בית
```bash
curl http://localhost:8000/
```

### 2. GET - קבלת כל המשימות
```bash
curl http://localhost:8000/todos
```

### 3. GET - קבלת משימות שהושלמו בלבד
```bash
curl "http://localhost:8000/todos?completed=true"
```

### 4. GET - קבלת משימות שלא הושלמו
```bash
curl "http://localhost:8000/todos?completed=false"
```

### 5. GET - קבלת משימה ספציפית
```bash
curl http://localhost:8000/todos/1
```

### 6. POST - יצירת משימה חדשה
```bash
curl -X POST http://localhost:8000/todos ^
  -H "Content-Type: application/json" ^
  -d "{\"title\": \"קנה חלב\", \"description\": \"מהסופר בקרבת מקום\", \"completed\": false}"
```

**גרסת PowerShell:**
```powershell
curl -Uri http://localhost:8000/todos -Method POST -ContentType "application/json" -Body '{"title": "קנה חלב", "description": "מהסופר בקרבת מקום", "completed": false}'
```

### 7. PUT - עדכון משימה
```bash
curl -X PUT http://localhost:8000/todos/1 ^
  -H "Content-Type: application/json" ^
  -d "{\"completed\": true}"
```

**גרסת PowerShell:**
```powershell
curl -Uri http://localhost:8000/todos/1 -Method PUT -ContentType "application/json" -Body '{"completed": true}'
```

### 8. DELETE - מחיקת משימה
```bash
curl -X DELETE http://localhost:8000/todos/1
```

**גרסת PowerShell:**
```powershell
curl -Uri http://localhost:8000/todos/1 -Method DELETE
```

---

## 📋 Lists API (`lists/main.py`)

### 1. GET - דף בית
```bash
curl http://localhost:8000/
```

### 2. GET - קבלת הודעה עם טקסט מותאם
```bash
curl http://localhost:8000/שלום
```

---

## 💡 טיפים שימושיים

### הצגת headers בתשובה
```bash
curl -i http://localhost:8000/
```

### הצגת verbose output (מידע מפורט)
```bash
curl -v http://localhost:8000/
```

### שמירת תשובה לקובץ
```bash
curl http://localhost:8000/todos -o todos.json
```

### שליחת headers מותאמים אישית
```bash
curl -H "Authorization: Bearer token123" http://localhost:8000/todos
```

### בדיקת זמן תגובה
```bash
curl -w "\nTime: %{time_total}s\n" http://localhost:8000/
```

---

## 🔍 בדיקת API Documentation

כל FastAPI מספק תיעוד אוטומטי:

### Swagger UI (אינטראקטיבי)
```bash
# פתח בדפדפן:
http://localhost:8000/docs
```

### ReDoc (קריאה)
```bash
# פתח בדפדפן:
http://localhost:8000/redoc
```

### OpenAPI Schema (JSON)
```bash
curl http://localhost:8000/openapi.json
```

---

## 🚀 הרצת השרתים

### Standard Example
```powershell
cd exampleStandart
python main.py
```

### Strings API
```powershell
cd strings
python main.py
```

### Todos API
```powershell
cd todos
uvicorn main:app --reload
```

### Lists API
```powershell
cd lists
python main.py
```

---

## ⚠️ פתרון בעיות נפוצות

### שגיאת Connection Refused
- וודא שהשרת רץ
- בדוק שהיציאה (port) נכונה

### שגיאת JSON Parse
- וודא שה-JSON תקין
- שים לב לציטוטים כפולים `"` בתוך ה-JSON
- ב-Windows, השתמש ב-`^` לשבירת שורות או הקלד הכל בשורה אחת

### Encoding Issues (עברית)
- ב-PowerShell, הוסף:
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```
