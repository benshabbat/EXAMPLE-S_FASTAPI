# FastAPI JSON Storage Demo

דוגמה מקיפה לעבודה עם JSON - שמירה, קריאה, עדכון ומחיקה.

## תכונות

- ✅ שמירת משתמשים ל-JSON
- ✅ שמירת הערות ל-JSON
- ✅ לוג פעילות אוטומטי
- ✅ גיבוי וייצוא נתונים
- ✅ ייבוא נתונים
- ✅ כל פעולות CRUD

## התקנה

```bash
pip install -r requirements.txt
```

## הרצה

```bash
python main.py
```

או:

```bash
uvicorn main:app --reload
```

## מבנה קבצים

הנתונים נשמרים בתיקייה `data/`:
- `users.json` - משתמשים
- `notes.json` - הערות
- `activity_log.json` - לוג פעילות
- `backup_*.json` - קבצי גיבוי

## דוגמאות שימוש

### משתמשים (Users)

#### יצירת משתמש
```bash
curl -X POST http://localhost:8000/users ^
  -H "Content-Type: application/json" ^
  -d "{\"name\": \"John Doe\", \"email\": \"john@example.com\", \"age\": 30}"
```

#### קבלת כל המשתמשים
```bash
curl http://localhost:8000/users
```

#### קבלת משתמש ספציפי
```bash
curl http://localhost:8000/users/1
```

#### עדכון משתמש
```bash
curl -X PUT http://localhost:8000/users/1 ^
  -H "Content-Type: application/json" ^
  -d "{\"name\": \"Jane Doe\", \"email\": \"jane@example.com\", \"age\": 28}"
```

#### מחיקת משתמש
```bash
curl -X DELETE http://localhost:8000/users/1
```

### הערות (Notes)

#### יצירת הערה
```bash
curl -X POST http://localhost:8000/notes ^
  -H "Content-Type: application/json" ^
  -d "{\"title\": \"My Note\", \"content\": \"This is a note\", \"tags\": [\"important\", \"work\"]}"
```

#### קבלת כל ההערות
```bash
curl http://localhost:8000/notes
```

#### עדכון חלקי של הערה
```bash
curl -X PATCH http://localhost:8000/notes/1 ^
  -H "Content-Type: application/json" ^
  -d "{\"content\": \"Updated content\"}"
```

### לוג פעילות

#### קבלת הלוג
```bash
curl http://localhost:8000/logs
```

#### ניקוי הלוג
```bash
curl -X DELETE http://localhost:8000/logs
```

### גיבוי וייצוא

#### יצירת גיבוי
```bash
curl -X POST http://localhost:8000/backup
```

#### ייצוא כל הנתונים
```bash
curl http://localhost:8000/export
```

#### ייבוא נתונים
```bash
curl -X POST http://localhost:8000/import ^
  -H "Content-Type: application/json" ^
  -d "{\"users\": [{\"id\": 1, \"name\": \"Test\"}], \"notes\": []}"
```

#### איפוס כל הנתונים
```bash
curl -X DELETE http://localhost:8000/reset
```

## תכונות מיוחדות

### שמירה אוטומטית
כל פעולה נשמרת מיד לקובץ JSON - אין צורך בשמירה ידנית.

### לוג אוטומטי
כל פעולה נרשמת אוטומטית ב-`activity_log.json` עם חותמת זמן.

### גיבוי
אפשר ליצור גיבוי מלא של כל הנתונים עם חותמת זמן.

### ייבוא וייצוא
אפשר לייצא את כל הנתונים או לייבא נתונים מקובץ JSON חיצוני.

## Swagger Documentation

גש ל-http://localhost:8000/docs לממשק אינטראקטיבי
