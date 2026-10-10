import requests

def test():
    # Login
    res = requests.post("http://127.0.0.1:8000/login", json={"username": "duyle", "password": "123"})
    if res.status_code != 200:
        res = requests.post("http://127.0.0.1:8000/login", json={"username": "duyle", "password": "123456"})
    if res.status_code != 200:
        print("Login failed:", res.text)
        return
        
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get chores
    res = requests.get("http://127.0.0.1:8000/chores", headers=headers)
    chores = res.json()
    if not chores:
        print("No chores")
        return
        
    chore_id = chores[0]["id"]
    print(f"Chore 0 user_order before: {chores[0].get('user_order')}")
    
    # Update order
    res = requests.put(f"http://127.0.0.1:8000/chores/{chore_id}/order", headers=headers, json={"user_order": [1]})
    print("Update status:", res.status_code, res.text)
    
    # Get chores again
    res = requests.get("http://127.0.0.1:8000/chores", headers=headers)
    chores_after = res.json()
    print(f"Chore 0 user_order after: {chores_after[0].get('user_order')}")

test()
