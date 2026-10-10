import urllib.request
import json

data = urllib.parse.urlencode({"username": "duyle", "password": "123"}).encode("utf-8")
req = urllib.request.Request("http://localhost:8000/login", data=data)
try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode())
        token = res["access_token"]
        
        req2 = urllib.request.Request("http://localhost:8000/chores", data=json.dumps({"name": "Test chore", "assignee_id": 1}).encode("utf-8"), headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req2) as res2:
                print(res2.getcode())
                print(res2.read().decode())
        except urllib.error.HTTPError as e:
            print("Error chores:", e.code, e.read().decode())
except urllib.error.HTTPError as e:
    print("Login error:", e.code, e.read().decode())
