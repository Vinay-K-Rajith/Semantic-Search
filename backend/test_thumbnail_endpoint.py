import requests

# Test thumbnail endpoint
url = "http://127.0.0.1:8000/thumbnails/Bio_X_LifeProcess_M6_ToShowThatChlorophyllIIsEssentialForPhotosynthesis.png"
r = requests.get(url)

print(f"Status: {r.status_code}")
print(f"Content-Type: {r.headers.get('content-type')}")
print(f"Size: {len(r.content)} bytes")
print(f"Valid PNG: {r.content[:8] == b'\\x89PNG\\r\\n\\x1a\\n'}")
