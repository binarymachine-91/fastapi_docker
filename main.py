from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Sample data to simulate a database
items = {
    1: {"name": "Item 1", "description": "This is the first item"},
    2: {"name": "Item 2", "description": "This is the second item"}
}

# GET request - fetch an item by its ID
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    item = items.get(item_id)
    if item:
        return {"item_id": item_id, "data": item}
    return {"error": "Item not found"}

# Data model for POST request using Pydantic
class Item(BaseModel):
    name: str
    description: str

# POST request - create a new item
@app.post("/items/")
async def create_item(item: Item):
    new_id = len(items) + 1
    items[new_id] = {"name": item.name, "description": item.description}
    return {"item_id": new_id, "data": items[new_id]}

