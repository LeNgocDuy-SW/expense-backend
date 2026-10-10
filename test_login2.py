import urllib.request
import urllib.error
import json

try:
    data = json.dumps({"username":"nguyen", "password":"password"}).encode()
    req = urllib.request.Request("http://127.0.0.1:8001/login", data=data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)
except urllib.error.HTTPError as e:
    print(e.read().decode())
