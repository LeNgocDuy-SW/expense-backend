from fastapi.testclient import TestClient
from app import app
import sys

client = TestClient(app)

res = client.post("/login", json={"username": "zqmzflxm", "password": "password123"})
if res.status_code == 200:
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    try:
        res2 = client.post("/chores", json={"name": "Test", "assignee_id": 1}, headers=headers)
        print("CHORE STATUS:", res2.status_code)
    except Exception as e:
        import traceback
        traceback.print_exc()
else:
    print("Login failed")
