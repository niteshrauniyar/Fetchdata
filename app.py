import requests
import time

session = requests.Session()

# Step 1: Hit homepage to get cookies
session.get("https://newweb.nepalstock.com")

url = "https://newweb.nepalstock.com/api/nots/nepse-data/floorsheet"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://newweb.nepalstock.com",
    "Referer": "https://newweb.nepalstock.com/floorsheet",
}

all_data = []

for page in range(1, 50):
    payload = {
        "page": page,
        "size": 500,
        "sortBy": "contractId",
        "sortOrder": "desc"
    }

    try:
        response = session.post(url, json=payload, headers=headers, timeout=10)

        if response.status_code != 200:
            print("Blocked at page:", page)
            break

        data = response.json()

        if not data.get("floorsheets"):
            break

        all_data.extend(data["floorsheets"])

        print(f"Page {page} fetched")

        time.sleep(0.5)  # 🔥 IMPORTANT (avoid blocking)

    except Exception as e:
        print("Error:", e)
        break

print("Total rows:", len(all_data))
