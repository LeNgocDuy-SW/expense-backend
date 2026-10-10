import requests
import json

res = requests.post("http://localhost:8000/login", json={"username": "duyle", "password": "123"})
if res.status_code == 200:
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    res2 = requests.post("http://localhost:8000/chores", json={"name": "Test chore", "assignee_id": 1}, headers=headers)
    print("Chores API status:", res2.status_code)
    print("Chores API response:", res2.text)
else:
    print("Login failed:", res.status_code, res.text)
