# מדריך - Path, Query ו-Body Parameters ב-FastAPI

## 🛣️ Path Parameters (פרמטרים במסלול)

**מה זה?** 
פרמטרים שהם **חלק מה-URL עצמו** - מופיעים בתוך ה-path.

**מתי משתמשים?**
- לזיהוי משאב ספציפי (למשל: מספר פריט, מספר משתמש)
- כשהפרמטר הוא **חובה** והוא מזהה ייחודי

**דוגמה:**
```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}
```

**קריאה:**
```
GET /items/123
```
כאן `123` הוא ה-Path Parameter.

---

## ❓ Query Parameters (פרמטרי שאילתא)

**מה זה?**
פרמטרים שמופיעים **אחרי סימן השאלה** ב-URL עם `?key=value&key2=value2`.

**מתי משתמשים?**
- לפילטור, מיון או חיפוש
- כשהפרמטרים **אופציונליים**
- כשיש הרבה פרמטרים שלא כולם חובה

**דוגמה:**
```python
@app.get("/items/search")
def search_items(
    min_price: int = Query(default=0),
    max_price: int = Query(default=1000),
    in_stock: bool = Query(default=None)
):
    return {"min_price": min_price, "max_price": max_price}
```

**קריאה:**
```
GET /items/search?min_price=50&max_price=150&in_stock=true
```

**חשוב:**
- `Query(...)` = חובה
- `Query(default=0)` = אופציונלי עם ברירת מחדל
- ללא `Query` זה גם עובד, אבל עם `Query` יש יותר אפשרויות

---

## 📦 Body Parameters (גוף הבקשה)

**מה זה?**
נתונים שנשלחים **בגוף הבקשה** (Request Body) בפורמט JSON.

**מתי משתמשים?**
- ב-POST, PUT, PATCH - כשיוצרים או מעדכנים נתונים
- כשיש **הרבה נתונים** או נתונים מורכבים
- כשהנתונים רגישים (לא רוצים שיופיעו ב-URL)

**דוגמה:**
```python
@app.post("/items")
def create_item(
    name: str = Body(...),
    description: str = Body(...),
    price: int = Body(...)
):
    return {"name": name, "price": price}
```

**קריאה:**
```bash
POST /items
Content-Type: application/json

{
    "name": "Laptop",
    "description": "Gaming laptop",
    "price": 3000
}
```

**חשוב:**
- `Body(...)` = חובה
- `Body(default=None)` = אופציונלי
- הנתונים נשלחים ב-JSON

---

## 🔀 שילוב של כולם ביחד!

```python
@app.post("/categories/{category_name}/items")
def create_item_in_category(
    category_name: str,              # Path Parameter
    priority: int = Query(default=1), # Query Parameter
    name: str = Body(...),            # Body Parameter
    price: int = Body(...)            # Body Parameter
):
    return {
        "category": category_name,
        "priority": priority,
        "name": name,
        "price": price
    }
```

**קריאה:**
```bash
POST /categories/electronics/items?priority=5
Content-Type: application/json

{
    "name": "Mouse",
    "price": 50
}
```

---

## 📊 טבלת השוואה

| סוג | איפה מופיע | מתי משתמשים | דוגמה |
|-----|-----------|-------------|-------|
| **Path** | בתוך ה-URL | זיהוי משאב, חובה | `/items/{id}` → `/items/123` |
| **Query** | אחרי `?` ב-URL | פילטור, חיפוש, אופציונלי | `/items?min_price=50&max_price=150` |
| **Body** | בגוף הבקשה (JSON) | יצירה/עדכון, נתונים מורכבים | `{"name": "Item", "price": 100}` |

---

## ✅ כללי אצבע

1. **Path** - למשאב ספציפי שחובה לזהות (id, username וכו')
2. **Query** - לפילטור, מיון, חיפוש - דברים אופציונליים
3. **Body** - ליצירה ועדכון של נתונים מורכבים

---

## 🎯 PUT vs PATCH

- **PUT** - עדכון **מלא** - צריך לשלוח את **כל השדות**
- **PATCH** - עדכון **חלקי** - שולחים רק את מה שרוצים לשנות

**דוגמה PUT:**
```json
{
    "name": "New Name",
    "description": "New Description",
    "price": 100,
    "in_stock": true
}
```

**דוגמה PATCH:**
```json
{
    "price": 100
}
```
רק המחיר יתעדכן!
