from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# Create FastAPI instance
app = FastAPI(
    title="Sample FastAPI Application",
    description="A simple FastAPI app for Docker deployment",
    version="1.0.0"
)

# Pydantic models
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    category: str

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    category: str

# In-memory storage (for demo purposes)
items_db = []
next_id = 1

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Docker Demo!", "status": "running"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fastapi-docker-app"}

# Get all items
@app.get("/items", response_model=List[ItemResponse])
async def get_items():
    return items_db

# Get item by ID
@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    item = next((item for item in items_db if item["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Create new item
@app.post("/items", response_model=ItemResponse)
async def create_item(item: Item):
    global next_id
    new_item = item.dict()
    new_item["id"] = next_id
    next_id += 1
    items_db.append(new_item)
    return new_item

# Update item
@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: Item):
    existing_item = next((item for item in items_db if item["id"] == item_id), None)
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    updated_item = item.dict()
    updated_item["id"] = item_id
    
    # Replace the item in the list
    for i, stored_item in enumerate(items_db):
        if stored_item["id"] == item_id:
            items_db[i] = updated_item
            break
    
    return updated_item

# Delete item
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    global items_db
    items_db = [item for item in items_db if item["id"] != item_id]
    return {"message": f"Item {item_id} deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)