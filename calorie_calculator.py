#  カロリー計算（1日の摂取目標カロリーを取得する）


import requests

BACKEND_URL = "https://your-vercel-backend-url.com"

def get_calorie_target(serial):
    payload = {"serial": serial}
    response = requests.post(f"{BACKEND_URL}/api/calorie-target", json=payload)
    # print("1日の摂取目標カロリー:", response.json().get("target_calories"))

if __name__ == "__main__":
    serial = open('/proc/cpuinfo').read().split("Serial")[1].split(":")[1].strip()
    get_calorie_target(serial)
