from fastapi import FastAPI
import redis

# connect to redis (make sure redis is running locally)
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Redis API is working!"}

# Set a key/value
@app.post("/set/{key}/{value}")
def set_key(key: str, value: str):
    r.set(key, value)
    return {"message": f"Key '{key}' set with value '{value}'"}

# Get a key/value
@app.get("/get/{key}")
def get_key(key: str):
    value = r.get(key)
    if value:
        return {"key": key, "value": value}
    else:
        return {"error": f"Key '{key}' not found"}
