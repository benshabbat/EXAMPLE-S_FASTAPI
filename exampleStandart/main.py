from fastapi import FastAPI, Query, Path, Body
from typing import Optional, Dict, Any
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="FastAPI Examples", version="1.0.0")

# ============================================
# דוגמה 1: GET פשוט
# ============================================
# הדוגמה הבסיסית ביותר - מחזיר JSON פשוט
# URL: http://localhost:8000/
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!", "status": "success"}


# ============================================
# דוגמה 2: GET עם path parameter
# ============================================
# Path parameter = ערך שנמצא בנתיב ה-URL עצמו
# item_id מוגדר כ-int, FastAPI יבצע validation אוטומטי
# URL: http://localhost:8000/items/5
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}"}


# ============================================
# דוגמה 3: GET עם query parameters
# ============================================
# Query parameters = פרמטרים שמגיעים אחרי ? ב-URL
# Optional[str] = None פירושו שהפרמטר לא חובה
# URL: http://localhost:8000/search?q=phone&skip=0&limit=10
@app.get("/search")
def search_items(
    q: Optional[str] = None,  # אופציונלי - חיפוש
    skip: int = 0,            # ברירת מחדל 0 - דילוג על תוצאות
    limit: int = 10           # ברירת מחדל 10 - מגבלת תוצאות
):
    return {
        "query": q,
        "skip": skip,
        "limit": limit,
        "results": ["item1", "item2", "item3"]
    }


# ============================================
# דוגמה 4: GET עם path ו-query parameters
# ============================================
# שילוב של path parameter (user_id) וquery parameters (skip, limit)
# Query(default=10, le=100) = ברירת מחדל 10, מקסימום 100
# URL: http://localhost:8000/users/1/items?skip=0&limit=5
@app.get("/users/{user_id}/items")
def read_user_items(
    user_id: int,                              # path parameter
    skip: int = 0,                             # query parameter
    limit: int = Query(default=10, le=100)     # query עם validation
):
    return {
        "user_id": user_id,
        "items": [f"item_{i}" for i in range(skip, skip + limit)]
    }


# ============================================
# מודל לדוגמאות POST
# ============================================
# BaseModel מ-Pydantic מספק validation אוטומטי
# Optional[str] = None פירושו שהשדה לא חובה
class Item(BaseModel):
    name: str                           # חובה
    description: Optional[str] = None   # אופציונלי
    price: float                        # חובה
    tax: Optional[float] = None         # אופציונלי


# ============================================
# דוגמה 5: POST עם request body
# ============================================
# מקבל JSON בגוף הבקשה וממיר אותו אוטומטית למודל Item
# model_dump() ממיר את המודל חזרה ל-dictionary
# Body: {"name": "Laptop", "price": 1200.0, "tax": 120.0}
@app.post("/items")
def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        # חישוב מחיר כולל מס
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# ============================================
# דוגמה 6: PUT לעדכון
# ============================================
# PUT משמש לעדכון מלא של resource קיים
# משלב path parameter (item_id) עם request body (item)
# URL: http://localhost:8000/items/5
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "updated_item": item.model_dump()}


# ============================================
# דוגמה 7: DELETE
# ============================================
# DELETE משמש למחיקת resource
# בדרך כלל מחזיר הודעת אישור
# URL: http://localhost:8000/items/5
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": f"Item {item_id} deleted successfully"}


# ============================================
# מודל למשתמש
# ============================================
class User(BaseModel):
    username: str                       # חובה
    email: str                          # חובה
    full_name: Optional[str] = None     # אופציונלי
    age: Optional[int] = None           # אופציונלי


# ============================================
# דוגמה 8: POST עם validation
# ============================================
# Pydantic מבצע validation אוטומטי על כל השדות
# אם username או email חסרים, תוחזר שגיאה 422
# Body: {"username": "john_doe", "email": "john@example.com", "age": 25}
@app.post("/users")
def create_user(user: User):
    return {
        "message": "User created successfully",
        "user": user.model_dump()
    }


# ============================================
# דוגמה 9: GET עם path validation
# ============================================
# Path(...) מאפשר להוסיף validation לpath parameter
# ge=1 (greater or equal) - לפחות 1
# le=1000 (less or equal) - מקסימום 1000
# URL: http://localhost:8000/products/50
@app.get("/products/{product_id}")
def get_product(
    product_id: int = Path(..., title="The ID of the product", ge=1, le=1000)
):
    return {
        "product_id": product_id,
        "name": f"Product {product_id}",
        "in_stock": True
    }


# ============================================
# דוגמה 10: Response עם status code מותאם
# ============================================
# status_code=201 = Created (נוצר resource חדש)
# ברירת המחדל היא 200 (OK)
# Body: {"username": "new_user", "email": "newuser@example.com"}
@app.post("/register", status_code=201)
def register_user(user: User):
    return {
        "message": "Registration successful",
        "user": user.model_dump()
    }


# ============================================
# דוגמה 11: טיפול במספר response models
# ============================================
# החזרת response שונה בהתאם לquery parameter
# URL: http://localhost:8000/info?detailed=true
@app.get("/info")
def get_info(detailed: bool = False):
    if detailed:
        return {
            "version": "1.0.0",
            "name": "FastAPI Examples",
            "description": "A collection of simple FastAPI examples",
            "endpoints": 11
        }
    return {"version": "1.0.0", "name": "FastAPI Examples"}


# ============================================
# דוגמה 12: List response
# ============================================
# החזרת רשימה (array) של objects
# שימושי לרשימות משתמשים, מוצרים וכו'
# URL: http://localhost:8000/users
@app.get("/users")
def get_users():
    return [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
    ]


# ============================================
# דוגמה 13: Header parameters
# ============================================
# קריאת ערכים מה-headers של הבקשה
# Header(...) מאפשר לקרוא headers כמו User-Agent, Authorization וכו'
# URL: http://localhost:8000/header-example
from fastapi import Header

@app.get("/header-example")
def read_header(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}


# ============================================
# דוגמה 14: Multiple body parameters
# ============================================
# קבלת יותר ממודל אחד ב-body
# FastAPI יצפה ל-JSON עם שני objects: "user" ו-"address"
# Body: {"user": {...}, "address": {...}}
class Address(BaseModel):
    street: str
    city: str
    country: str

@app.post("/user-with-address")
def create_user_with_address(user: User, address: Address):
    return {
        "user": user.model_dump(),
        "address": address.model_dump()
    }


# ============================================
# דוגמה 15: Response model
# ============================================
# response_model מגדיר איך התגובה תיראה בתיעוד
# מבטיח שהתגובה תואמת למבנה המוגדר
# URL: http://localhost:8000/items-list
from fastapi import Response

@app.get("/items-list", response_model=list[Item])
def get_items_list():
    return [
        Item(name="Item 1", price=10.5),
        Item(name="Item 2", price=20.0, tax=2.0)
    ]


# ============================================
# דוגמה 16: File upload
# ============================================
# UploadFile מאפשר העלאת קבצים
# async כי קריאת קבצים היא פעולה אסינכרונית
# שימוש: בחר קובץ ב-multipart/form-data
from fastapi import File, UploadFile

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.size
    }


# ============================================
# דוגמה 17: Form data
# ============================================
# Form(...) מקבל נתונים מטופס HTML (application/x-www-form-urlencoded)
# שונה מ-Body שמקבל JSON
# שימושי לטפסי התחברות, רישום וכו'
from fastapi import Form

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "message": "Login successful"}


# ============================================
# דוגמה 18: Cookie parameters
# ============================================
# Cookie(...) מקרא cookies מהדפדפן
# שימושי ל-session management, authentication
# URL: http://localhost:8000/cookie-example
from fastapi import Cookie

@app.get("/cookie-example")
def read_cookie(session_id: Optional[str] = Cookie(None)):
    return {"session_id": session_id}


# ============================================
# דוגמה 19: HTTPException
# ============================================
# HTTPException מאפשר להחזיר שגיאות HTTP עם status code מותאם
# 404 = Not Found, 400 = Bad Request, 403 = Forbidden וכו'
# URL: http://localhost:8000/items-check/150 (תחזיר 404)
from fastapi import HTTPException

@app.get("/items-check/{item_id}")
def get_item_with_check(item_id: int):
    if item_id > 100:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "name": f"Item {item_id}"}


# ============================================
# דוגמה 20: Background tasks
# ============================================
# BackgroundTasks מאפשר הרצת משימות ברקע אחרי החזרת התגובה
# שימושי לשליחת מיילים, logging, עיבוד כבד וכו'
# המשימה תרוץ אחרי שהתגובה נשלחת ללקוח
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", "a") as log:
        log.write(f"{message}\n")

@app.post("/send-notification/{email}")
def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    return {"message": "Notification will be sent"}


# ============================================
# דוגמה 21: Dependency injection
# ============================================
# Depends(...) מאפשר לעשות reuse של לוגיקה משותפת
# הפונקציה common_parameters תרוץ אוטומטית ותזריק את התוצאה
# שימושי לאימות, בדיקות הרשאה, פרמטרים משותפים
# URL: http://localhost:8000/dependency-example?skip=5&limit=20
from fastapi import Depends

def common_parameters(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/dependency-example")
def read_with_dependency(commons: dict = Depends(common_parameters)):
    return commons


# ============================================
# דוגמה 22: Tags לארגון בתיעוד
# ============================================
# tags מקבצים endpoints בתיעוד האוטומטי (Swagger)
# עוזר לארגן API גדול לקטגוריות
# בתיעוד יופיעו תחת "admin" ו-"public"
@app.get("/admin/users", tags=["admin"])
def get_admin_users():
    return {"users": ["admin1", "admin2"]}

@app.get("/public/posts", tags=["public"])
def get_public_posts():
    return {"posts": ["post1", "post2", "post3"]}


# ============================================
# דוגמה 23: Body בלי Pydantic - Dict פשוט
# ============================================
# Dict[str, Any] מקבל כל JSON שנשלח
# אין validation אוטומטי - מקבל הכל
# שימושי כשהמבנה משתנה או לא ידוע מראש
# Body: {"any": "data", "you": "want", "number": 123}
@app.post("/raw-body")
def create_with_dict(data: Dict[str, Any] = Body(...)):
    return {
        "received": data,
        "type": "raw dictionary"
    }


# ============================================
# דוגמה 24: Body עם ערכים ספציפיים בלי מודל
# ============================================
# במקום מודל שלם, מקבלים שדות בודדים
# Body(...) מסמן שהשדה חייב להגיע מה-body
# Body(None) מסמן שהשדה אופציונלי
# Body: {"name": "Product", "price": 99.9, "description": "Nice"}
@app.post("/simple-body")
def create_simple(
    name: str = Body(...),              # חובה
    price: float = Body(...),           # חובה
    description: Optional[str] = Body(None)  # אופציונלי
):
    return {
        "name": name,
        "price": price,
        "description": description
    }


# ============================================
# דוגמה 25: Body עם embed
# ============================================
# embed=True גורם ל-FastAPI לצפות ש-JSON יהיה עטוף ב-object
# בלי embed: {"key": "value"}
# עם embed: {"item": {"key": "value"}}
# Body: {"item": {"key": "value", "another": 123}}
@app.post("/embedded-body")
def create_embedded(item: Dict[str, Any] = Body(..., embed=True)):
    return {"item_received": item}


# ============================================
# דוגמה 26: Multiple raw body parameters
# ============================================
# קבלת כמה dictionaries שונים ב-body
# FastAPI יצפה ל-JSON עם שני keys: "data" ו-"metadata"
# Body: {"data": {...}, "metadata": {...}}
@app.post("/multiple-raw-bodies")
def multiple_bodies(
    data: Dict[str, Any] = Body(...),
    metadata: Dict[str, Any] = Body(...)
):
    return {
        "data": data,
        "metadata": metadata
    }


# ============================================
# דוגמה 27: Body עם ברירת מחדל
# ============================================
# ניתן לתת ערכי ברירת מחדל לפרמטרים
# אם לא נשלחים, ישתמשו בערכים אלו
# Body: {} (ריק) או {"name": "Custom Name"}
@app.post("/body-with-default")
def body_with_default(
    name: str = Body("Default Name"),
    age: int = Body(18),
    active: bool = Body(True)
):
    return {
        "name": name,
        "age": age,
        "active": active
    }


# ============================================
# דוגמה 28: List בתור Body
# ============================================
# קבלת רשימה ישירות ב-body (לא object)
# שימושי לקבלת מערכים של מספרים, strings וכו'
# Body: [1, 2, 3, 4, 5] או ["item1", "item2"]
@app.post("/list-body")
def create_list(items: list = Body(...)):
    return {
        "count": len(items),
        "items": items
    }


# ============================================
# הרצת השרת
# ============================================
# הקוד הזה מריץ את השרת רק כשמריצים את הקובץ ישירות
# python main.py = יריץ שרת על פורט 8000
# uvicorn main:app --reload = דרך אחרת להרצה (מומלץ לפיתוח)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
