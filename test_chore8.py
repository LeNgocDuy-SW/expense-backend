import requests
res = requests.post("http://localhost:8000/login", json={"username": "zqmzflxm", "password": "password123"})
if res.status_code == 200:
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    res2 = requests.post("http://localhost:8000/chores", json={"name": "Test", "assignee_id": 1}, headers=headers)
    print("CHORE:", res2.status_code, res2.content.decode('utf-8', errors='ignore'))
else:
    print("LOGIN FAILED", res.status_code, res.content.decode('utf-8', errors='ignore'))
