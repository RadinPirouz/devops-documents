# Python + Redis Quick Guide

This document explains how to set up Python, connect to Redis, and perform basic cache operations.

---

## 1. Setup

Install Python and create a virtual environment:

```bash
sudo apt install python3-full
python3 -m venv .venv
source .venv/bin/activate
```

---

## 2. Connect and Test Redis Connection

```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0)
print(r.ping())  # Should print True
```

**Expected Output:**

```
True
```

---

## 3. Caching Scenario Example

This example demonstrates caching data in Redis with a TTL (Time To Live).

```python
import redis
import time

r = redis.Redis(host='localhost', port=6379, db=0)

def get_data_from_db():
    print("Fetching from DB...")
    time.sleep(2)  # Simulate slow query
    return {"user": "alice", "age": 30}

def get_user(user_id):
    cache_key = f"user:{user_id}"
    
    # Check cache first
    cached = r.get(cache_key)
    if cached:
        print("Cache hit")
        return eval(cached)
    
    # Fetch from DB
    data = get_data_from_db()
    
    # Store in Redis with TTL (10 seconds)
    r.set(cache_key, str(data), ex=10)
    return data

print(get_user(1))
print(get_user(1))  # Should hit cache
```

---

## 4. Connect, Set, and Get Example

```python
import redis

r = redis.Redis(host="192.168.6.160", port=6379, db=0)

r.set('name', 'radin')

name = r.get('name')
print(name)
print(name.decode("utf-8"))
```

---

## 5. Interactive Read/Write Example

```python
import redis

method = int(input("Enter Method: (1.Read/2.Write) "))

r = redis.Redis(host="192.168.6.160", port=6379, db=0)

if method == 1:
    key = str(input("Enter key name: "))
    value = r.get(key)
    if value is None:
        print("Undefined Key")
    else:
        print(value)
elif method == 2:
    key = str(input("Enter key name: "))
    value = str(input("Enter value: "))
    r.set(key, value)
else:
    print("Incorrect Input")
```

---

## 6. Professional Version (Improved Code)

```python
import redis
import sys

def connect_redis(host="192.168.6.160", port=6379, db=0):
    """Establish a connection to Redis."""
    try:
        client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        # Test connection
        client.ping()
        return client
    except redis.ConnectionError as e:
        print(f"Error connecting to Redis: {e}")
        sys.exit(1)

def read_key(client):
    """Read a key from Redis."""
    key = input("Enter key name: ").strip()
    value = client.get(key)
    if value is None:
        print("Undefined Key")
    else:
        print(f"Value: {value}")

def write_key(client):
    """Write a key-value pair to Redis."""
    key = input("Enter key name: ").strip()
    value = input("Enter value: ").strip()
    client.set(key, value)
    print(f"Successfully set key '{key}' with value '{value}'.")

def main():
    client = connect_redis()

    print("Select Method:")
    print("1. Read")
    print("2. Write")
    
    try:
        method = int(input("Enter method (1 or 2): ").strip())
    except ValueError:
        print("Invalid input. Please enter 1 or 2.")
        sys.exit(1)

    if method == 1:
        read_key(client)
    elif method == 2:
        write_key(client)
    else:
        print("Incorrect input. Please enter 1 or 2.")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

