import requests
import json
import random
import string

def r_str():
    return ''.join(random.choices(string.ascii_lowercase, k=8))

username = r_str()
print("Username:", username)
# 1. Register
res = requests.post("http://localhost:8000/register", json={"username": username, "password": "password123", "display_name": "Test"})
if res.status_code != 200:
    print("Register failed:", res.status_code, res.text)
    exit()

# 2. Login
res = requests.post("http://localhost:8000/login", json={"username": username, "password": "password123"})
if res.status_code != 200:
    print("Login failed:", res.status_code, res.text)
    exit()
token = res.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print("Logged in")

# 3. Create room
res = requests.post("http://localhost:8000/rooms", json={"name": "Test Room"}, headers=headers)
if res.status_code != 200:
    print("Room failed:", res.status_code, res.text)
    exit()
print("Room created")

# 4. Get me to get my ID
res = requests.get("http://localhost:8000/me", headers=headers)
my_id = res.json()["id"]

# 5. Create chore
res = requests.post("http://localhost:8000/chores", json={"name": "Test chore API", "assignee_id": my_id}, headers=headers)
print("Chore API status:", res.status_code)
print("Chore API response:", res.text)
