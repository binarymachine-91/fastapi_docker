from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error

app = FastAPI()

# MySQL Database connection configuration
db_config = {
    'host': '172.17.0.2',
    'user': 'root',  # Replace with your MySQL username
    'password': 'pass',  # Replace with your MySQL password
    'database': 'dummy',
    'port': 3306
}


# Pydantic model to handle POST data
class Item(BaseModel):
    name: str
    description: str


# Function to get a database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")


# GET request to fetch all items
@app.get("/")
async def home_page():
    return "Welcome to Docker world!"

@app.get("/items/")
async def get_items():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM items"
    cursor.execute(query)
    items = cursor.fetchall()
    cursor.close()
    connection.close()
    return items


# POST request to create a new item
@app.post("/items/")
async def create_item(item: Item):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO items (name, description) VALUES (%s, %s)"
    values = (item.name, item.description)

    try:
        cursor.execute(query, values)
        connection.commit()
        item_id = cursor.lastrowid
    except Error as e:
        connection.rollback()
        cursor.close()
        connection.close()
        raise HTTPException(status_code=500, detail="Failed to insert item")

    cursor.close()
    connection.close()

    return {"id": item_id, "name": item.name, "description": item.description}
