import requests
res = requests.post("http://localhost:8000/login", json={"username": "duyle", "password": "123"})
token = res.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
res2 = requests.get("http://localhost:8000/chores", headers=headers)
chores = res2.json()
if chores:
    c = chores[0]
    res3 = requests.put(f"http://localhost:8000/chores/{c['id']}/order", json={"user_order": [4, 2, 1, 3]}, headers=headers)
    print("PUT status:", res3.status_code)
    res4 = requests.get("http://localhost:8000/chores", headers=headers)
    print("After PUT:", res4.json()[0].get("user_order"))
