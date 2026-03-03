import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Test search query
response = requests.post(f"{BASE_URL}/search", json={"query": "chlorophyll", "top_k": 3}, timeout=30)
data = response.json()

print("=" * 80)
print(f"Query: {data['query']}")
print(f"Total Results: {data['total']}")
print(f"Time: {data['time_ms']}ms")
print("=" * 80)

for i, result in enumerate(data['results'], 1):
    print(f"\n{i}. Caption: {result['caption']}")
    print(f"   Subtopic: {result['subtopic']}")
    print(f"   File: {result['file_name']}")
    print(f"   Thumbnail: '{result['thumbnail']}'")
    print(f"   Thumbnail Type: {type(result['thumbnail'])}")
    print(f"   Thumbnail Length: {len(result['thumbnail']) if result['thumbnail'] else 0}")
    print(f"   Score: {result['score']}")

print("\n" + "=" * 80)
