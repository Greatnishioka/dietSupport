import requests
from config import BACKEND_URL
from cpu_serial import get_cpu_serial

def get_calorie_target():
    serial = get_cpu_serial()
    
    if not serial:
        print("Error: Could not retrieve CPU serial number.")
        return
    
    payload = {"serial": serial}
    print(f"Sending request with payload: {payload}")

    try:
        response = requests.post(
            "https://diet-support.lugongdao07.workers.dev/analyze",
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        print("Target calorie:", response.json().get("target_calories"))
    except requests.exceptions.RequestException as e:
        print("Error:", e)

if __name__ == "__main__":
    get_calorie_target()

