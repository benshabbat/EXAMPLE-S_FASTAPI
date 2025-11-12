from fastapi import FastAPI, Request

app = FastAPI()

# מאגר דמו פשוט
items = {
    1: {"id": 1, "name": "Item 1", "price": 10.5},
    2: {"id": 2, "name": "Item 2", "price": 20.0},
}

@app.get("/")
def read_root():
    """דף הבית"""
    return {"message": "FastAPI HTTP Methods Demo"}

@app.get("/items")
def get_all_items():
    """GET - קבלת כל הפריטים"""
    return {"items": list(items.values())}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    """GET - קבלת פריט לפי ID"""
    if item_id in items:
        return items[item_id]
    return {"error": "Item not found"}, 404

@app.post("/items")
async def create_item(request: Request):
    """POST - יצירת פריט חדש"""
    body = await request.json()
    new_id = max(items.keys()) + 1 if items else 1
    new_item = {
        "id": new_id,
        "name": body.get("name", "Unknown"),
        "price": body.get("price", 0.0)
    }
    items[new_id] = new_item
    return {"message": "Item created", "item": new_item}

@app.put("/items/{item_id}")
async def update_item_full(item_id: int, request: Request):
    """PUT - עדכון מלא של פריט (מחליף את כל השדות)"""
    body = await request.json()
    if item_id not in items:
        return {"error": "Item not found"}, 404
    
    items[item_id] = {
        "id": item_id,
        "name": body.get("name", "Unknown"),
        "price": body.get("price", 0.0)
    }
    return {"message": "Item fully updated", "item": items[item_id]}

@app.patch("/items/{item_id}")
async def update_item_partial(item_id: int, request: Request):
    """PATCH - עדכון חלקי של פריט (רק שדות שנשלחו)"""
    body = await request.json()
    if item_id not in items:
        return {"error": "Item not found"}, 404
    
    # עדכון רק השדות שנשלחו
    if "name" in body:
        items[item_id]["name"] = body["name"]
    if "price" in body:
        items[item_id]["price"] = body["price"]
    
    return {"message": "Item partially updated", "item": items[item_id]}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """DELETE - מחיקת פריט"""
    if item_id not in items:
        return {"error": "Item not found"}, 404
    
    deleted_item = items.pop(item_id)
    return {"message": "Item deleted", "item": deleted_item}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
