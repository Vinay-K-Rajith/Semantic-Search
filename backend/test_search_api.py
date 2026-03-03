import requests
import json

URL = "http://localhost:8000/search"
payload = {"query": "fractions", "top_k": 3}

try:
    resp = requests.post(URL, json=payload)
    print(f"Status Code: {resp.status_code}")
    if resp.status_code == 200:
        print(json.dumps(resp.json(), indent=2))
    else:
        print(resp.text)
except Exception as e:
    print(f"Error: {e}")
