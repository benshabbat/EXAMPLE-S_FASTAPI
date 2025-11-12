from fastapi import FastAPI, HTTPException, Body, Query

app = FastAPI()

# Database mock - רשימה פשוטה במקום מסד נתונים
items = [
    {"id": 1, "name": "Item 1", "description": "First item", "price": 100, "in_stock": True},
    {"id": 2, "name": "Item 2", "description": "Second item", "price": 200, "in_stock": False},
]

# ============================================
# GET EXAMPLES - דוגמאות ל-GET
# ============================================

# GET - קבלת כל הפריטים (ללא פרמטרים)
@app.get("/items")
def get_all_items():
    """
    Path: /items
    לא מקבל פרמטרים
    """
    return {"items": items}

# GET - עם Query Parameters (פרמטרים בשאילתא)
@app.get("/items/search")
def search_items(
    min_price: int = Query(default=0, description="מחיר מינימלי"),
    max_price: int = Query(default=1000, description="מחיר מקסימלי"),
    in_stock: bool = Query(default=None, description="האם במלאי")
):
    """
    Path: /items/search
    Query Parameters: ?min_price=50&max_price=150&in_stock=true
    
    דוגמה: /items/search?min_price=50&max_price=150&in_stock=true
    """
    filtered_items = []
    for item in items:
        if item["price"] >= min_price and item["price"] <= max_price:
            if in_stock is None or item["in_stock"] == in_stock:
                filtered_items.append(item)
    return {"items": filtered_items, "count": len(filtered_items)}

# GET - עם Path Parameter (פרמטר במסלול)
@app.get("/items/{item_id}")
def get_item(item_id: int):
    """
    Path: /items/{item_id}
    Path Parameter: item_id הוא חלק מה-URL
    
    דוגמה: /items/1
    """
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# GET - שילוב של Path Parameter ו-Query Parameters
@app.get("/items/{item_id}/details")
def get_item_with_options(
    item_id: int,  # Path Parameter
    include_price: bool = Query(default=True, description="האם להציג מחיר"),
    include_stock: bool = Query(default=True, description="האם להציג מלאי")
):
    """
    Path: /items/{item_id}/details
    Path Parameter: item_id
    Query Parameters: ?include_price=true&include_stock=false
    
    דוגמה: /items/1/details?include_price=true&include_stock=false
    """
    for item in items:
        if item["id"] == item_id:
            result = {"id": item["id"], "name": item["name"], "description": item["description"]}
            if include_price:
                result["price"] = item["price"]
            if include_stock:
                result["in_stock"] = item["in_stock"]
            return result
    raise HTTPException(status_code=404, detail="Item not found")

# ============================================
# POST EXAMPLES - דוגמאות ל-POST
# ============================================

# POST - עם Query Parameters (פשוט)
@app.post("/items/simple")
def create_item_simple(
    name: str = Query(..., description="שם הפריט"),
    description: str = Query(..., description="תיאור הפריט")
):
    """
    Path: /items/simple
    Query Parameters: ?name=NewItem&description=NewDescription
    
    דוגמה: POST /items/simple?name=NewItem&description=NewDescription
    """
    new_id = max([item["id"] for item in items]) + 1 if items else 1
    new_item = {"id": new_id, "name": name, "description": description, "price": 0, "in_stock": True}
    items.append(new_item)
    return {"message": "Item created", "item": new_item}

# POST - עם Body (JSON) - הדרך המומלצת!
@app.post("/items")
def create_item(
    name: str = Body(..., description="שם הפריט"),
    description: str = Body(..., description="תיאור הפריט"),
    price: int = Body(..., description="מחיר"),
    in_stock: bool = Body(default=True, description="האם במלאי")
):
    """
    Path: /items
    Body (JSON): שולחים את הנתונים בגוף הבקשה
    
    דוגמה:
    POST /items
    Body: {
        "name": "New Item",
        "description": "New Description",
        "price": 150,
        "in_stock": true
    }
    """
    new_id = max([item["id"] for item in items]) + 1 if items else 1
    new_item = {
        "id": new_id,
        "name": name,
        "description": description,
        "price": price,
        "in_stock": in_stock
    }
    items.append(new_item)
    return {"message": "Item created", "item": new_item}

# POST - שילוב של Path, Query ו-Body
@app.post("/categories/{category_name}/items")
def create_item_in_category(
    category_name: str,  # Path Parameter
    priority: int = Query(default=1, description="עדיפות"),  # Query Parameter
    name: str = Body(...),  # Body
    description: str = Body(...),  # Body
    price: int = Body(...)  # Body
):
    """
    Path: /categories/{category_name}/items
    Path Parameter: category_name
    Query Parameter: ?priority=5
    Body: JSON עם name, description, price
    
    דוגמה:
    POST /categories/electronics/items?priority=5
    Body: {
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": 3000
    }
    """
    new_id = max([item["id"] for item in items]) + 1 if items else 1
    new_item = {
        "id": new_id,
        "name": name,
        "description": description,
        "price": price,
        "in_stock": True,
        "category": category_name,
        "priority": priority
    }
    items.append(new_item)
    return {"message": "Item created in category", "item": new_item}

# ============================================
# PUT EXAMPLE - דוגמה ל-PUT
# ============================================

# PUT - עדכון מלא (בדרך כלל עם Body)
@app.put("/items/{item_id}")
def update_item(
    item_id: int,  # Path Parameter
    name: str = Body(...),
    description: str = Body(...),
    price: int = Body(...),
    in_stock: bool = Body(...)
):
    """
    Path: /items/{item_id}
    Path Parameter: item_id
    Body: JSON עם כל השדות (עדכון מלא!)
    
    דוגמה:
    PUT /items/1
    Body: {
        "name": "Updated Item",
        "description": "Updated Description",
        "price": 250,
        "in_stock": true
    }
    """
    for item in items:
        if item["id"] == item_id:
            item["name"] = name
            item["description"] = description
            item["price"] = price
            item["in_stock"] = in_stock
            return {"message": "Item fully updated", "item": item}
    raise HTTPException(status_code=404, detail="Item not found")

# ============================================
# PATCH EXAMPLE - דוגמה ל-PATCH
# ============================================

# PATCH - עדכון חלקי (רק השדות שמועברים)
@app.patch("/items/{item_id}")
def partial_update_item(
    item_id: int,  # Path Parameter
    name: str = Body(default=None),
    description: str = Body(default=None),
    price: int = Body(default=None),
    in_stock: bool = Body(default=None)
):
    """
    Path: /items/{item_id}
    Path Parameter: item_id
    Body: JSON עם רק השדות שרוצים לעדכן (עדכון חלקי!)
    
    דוגמה:
    PATCH /items/1
    Body: {
        "price": 300
    }
    רק המחיר יתעדכן, שאר השדות יישארו כפי שהם
    """
    for item in items:
        if item["id"] == item_id:
            if name is not None:
                item["name"] = name
            if description is not None:
                item["description"] = description
            if price is not None:
                item["price"] = price
            if in_stock is not None:
                item["in_stock"] = in_stock
            return {"message": "Item partially updated", "item": item}
    raise HTTPException(status_code=404, detail="Item not found")

# ============================================
# DELETE EXAMPLE - דוגמה ל-DELETE
# ============================================

# DELETE - מחיקה (בדרך כלל רק עם Path Parameter)
@app.delete("/items/{item_id}")
def delete_item(
    item_id: int,  # Path Parameter
    confirm: bool = Query(default=False, description="אישור מחיקה")  # Query Parameter נוסף
):
    """
    Path: /items/{item_id}
    Path Parameter: item_id
    Query Parameter (אופציונלי): ?confirm=true
    
    דוגמה:
    DELETE /items/1?confirm=true
    """
    if not confirm:
        raise HTTPException(status_code=400, detail="Please confirm deletion with ?confirm=true")
    
    for i, item in enumerate(items):
        if item["id"] == item_id:
            deleted_item = items.pop(i)
            return {"message": "Item deleted", "item": deleted_item}
    raise HTTPException(status_code=404, detail="Item not found")
