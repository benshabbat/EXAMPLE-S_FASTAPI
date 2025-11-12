# Basic CRUD Operations - FastAPI Example

דוגמה פשוטה לכל שיטות ה-HTTP הבסיסיות ללא Pydantic.

## התקנה

```bash
pip install -r requirements.txt
```

## הרצה

```bash
uvicorn main:app --reload
```

## API Endpoints

### GET - קבלת כל הפריטים
```bash
curl http://localhost:8000/items
```

### GET - קבלת פריט בודד
```bash
curl http://localhost:8000/items/1
```

### POST - יצירת פריט חדש
```bash
curl -X POST "http://localhost:8000/items?name=New Item&description=New Description"
```

### PUT - עדכון מלא של פריט
```bash
curl -X PUT "http://localhost:8000/items/1?name=Updated Item&description=Updated Description"
```

### PATCH - עדכון חלקי של פריט
```bash
curl -X PATCH "http://localhost:8000/items/1?name=Partially Updated"
```

### DELETE - מחיקת פריט
```bash
curl -X DELETE "http://localhost:8000/items/1"
```

## גישה לתיעוד אינטראקטיבי

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
