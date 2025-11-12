# FastAPI HTTP Methods Demo

דוגמה פשוטה לכל מתודות HTTP ללא Pydantic.

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

השרת יעלה על: http://localhost:8000

## דוגמאות שימוש

### GET - קבלת כל הפריטים
```bash
curl http://localhost:8000/items
```

### GET - קבלת פריט לפי ID
```bash
curl http://localhost:8000/items/1
```

### POST - יצירת פריט חדש
```bash
curl -X POST http://localhost:8000/items ^
  -H "Content-Type: application/json" ^
  -d "{\"name\": \"New Item\", \"price\": 15.5}"
```

### PUT - עדכון מלא של פריט
```bash
curl -X PUT http://localhost:8000/items/1 ^
  -H "Content-Type: application/json" ^
  -d "{\"name\": \"Updated Item\", \"price\": 25.0}"
```

### PATCH - עדכון חלקי של פריט
```bash
curl -X PATCH http://localhost:8000/items/1 ^
  -H "Content-Type: application/json" ^
  -d "{\"price\": 30.0}"
```

### DELETE - מחיקת פריט
```bash
curl -X DELETE http://localhost:8000/items/1
```

## הבדל בין PUT ל-PATCH

- **PUT**: מחליף את כל האובייקט (צריך לשלוח את כל השדות)
- **PATCH**: מעדכן רק את השדות שנשלחו

## Swagger Documentation

גש ל-http://localhost:8000/docs לממשק אינטראקטיבי
