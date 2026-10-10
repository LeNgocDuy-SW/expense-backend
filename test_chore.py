import requests

def test():
    res = requests.post("http://127.0.0.1:8000/login", json={"username": "duyle", "password": "123"})
    if res.status_code != 200:
        res = requests.post("http://127.0.0.1:8000/login", json={"username": "duyle", "password": "123456"})
        
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    res = requests.get("http://127.0.0.1:8000/chores", headers=headers)
    chores = res.json()
    chore = chores[0]
    uo = chore.get("user_order")
    print("type:", type(uo), "value:", uo)

test()
