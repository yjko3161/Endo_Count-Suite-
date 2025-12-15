import requests
import time

url = "http://127.0.0.1:5000/non_existent_page_to_trigger_404"

print("Starting scanner simulation...")
for i in range(1, 10):
    try:
        response = requests.get(url)
        print(f"Request {i}: Status Code {response.status_code}")
        if response.status_code == 403:
            print("SUCCESS: Blocked (403 Forbidden) received.")
            break
    except Exception as e:
        print(f"Request {i} failed: {e}")
    time.sleep(0.1)

print("Simulation complete.")
