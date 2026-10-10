import requests
res = requests.post("http://localhost:8000/login", json={"username": "duyle", "password": "123"})
print(res.status_code, res.text)
