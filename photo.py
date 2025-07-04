import requests
import os

os.makedirs("real_faces", exist_ok=True)

for i in range(1, 1001):
    response = requests.get("https://thispersondoesnotexist.com", headers={"User-Agent": "Mozilla/5.0"})
    with open(f"real_faces/face_{i}.jpg", "wb") as f:
        f.write(response.content)
    print(f"Downloaded face_{i}.jpg")
