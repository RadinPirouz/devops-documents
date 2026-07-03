from fastapi import FastAPI
from pydantic import BaseModel
import redis

# Connect to Redis
r = redis.Redis(host="192.168.6.160", port=30553, db=0, decode_responses=True)

app = FastAPI()

# For sending JSON data
class Item(BaseModel):
    key: str
    value: str | None = None   # make value optional

@app.get("/")
def home():
    return {"message": "Redis API is working!"}

# Set key/value using JSON body
@app.post("/set")
def set_json(item: Item):
    r.set(item.key, item.value)
    return {"message": f"Saved {item.key} = {item.value}"}

@app.post("/get")
def get_json(item: Item):
    value = r.get(item.key)
    return {"Key": f"{value}"}