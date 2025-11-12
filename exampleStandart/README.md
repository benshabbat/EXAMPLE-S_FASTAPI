# דוגמאות FastAPI פשוטות

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

## נקודות קצה (Endpoints)

### 1. GET / - דף בית פשוט
```
http://localhost:8000/
```

### 2. GET /items/{item_id} - Path Parameter
```
http://localhost:8000/items/5
```

### 3. GET /search - Query Parameters
```
http://localhost:8000/search?q=phone&skip=0&limit=10
```

### 4. GET /users/{user_id}/items - Path + Query
```
http://localhost:8000/users/1/items?skip=0&limit=5
```

### 5. POST /items - יצירת פריט חדש
```json
{
    "name": "Laptop",
    "description": "Gaming laptop",
    "price": 1200.00,
    "tax": 120.00
}
```

### 6. PUT /items/{item_id} - עדכון פריט
```json
{
    "name": "Updated Laptop",
    "price": 1300.00
}
```

### 7. DELETE /items/{item_id} - מחיקת פריט
```
http://localhost:8000/items/5
```

### 8. POST /users - יצירת משתמש
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "age": 25
}
```

### 9. GET /products/{product_id} - עם Validation
```
http://localhost:8000/products/50
```

### 10. POST /register - רישום עם Status Code 201
```json
{
    "username": "new_user",
    "email": "newuser@example.com"
}
```

### 11. GET /info - Response מותאם
```
http://localhost:8000/info?detailed=true
```

## תיעוד אוטומטי

FastAPI יוצר תיעוד אוטומטי:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## טיפים

1. השתמש ב-`--reload` בזמן פיתוח לטעינה אוטומטית של שינויים
2. בדוק את התיעוד האינטראקטיבי ב-`/docs`
3. כל ה-endpoints תומכים ב-validation אוטומטי
4. Pydantic מטפל באופן אוטומטי בהמרת טיפוסים
