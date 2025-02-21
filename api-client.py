# 画像をAPIに送信する

import requests

def send_fridge_data(image_path):
    # send imformation to API
    files = {'file': open(image_path, 'rb')}
    response = requests.post("https://your-api.com/fridge", files=files)
    if response.status_code == 200:
        print("successful")
