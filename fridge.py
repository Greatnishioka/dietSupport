import cv2
import requests
import base64
import os
import time
import RPi.GPIO as GPIO
from picamera2 import Picamera2
from datetime import datetime
from config import BACKEND_URL, DOOR_SENSOR_PIN, IMAGE_PATH
from cpu_serial import get_cpu_serial



def init_db():
    conn = sqlite3.connect("calories.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calorie_intakes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food TEXT,
            date TEXT,
            calorie INTEGER
        )
    """)
    conn.commit()
    conn.close()


def save_calorie_data(food, date, calorie):
    conn = sqlite3.connect("calories.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO calorie_intakes (food, date, calorie)
        VALUES (?, ?, ?)
    """, (food, date, calorie))
    conn.commit()
    conn.close()


# GPIO setup
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# take pictures
def capture_image():
    camera = Picamera2()
    config = camera.create_still_configuration()  
    camera.configure(config)  
    camera.start()
    time.sleep(2) 
    print(f"Capturing image to {IMAGE_PATH}...")
    camera.capture_file(IMAGE_PATH)
    print("Image captured successfully.")
    camera.close()
   
    
    

#  send image to backend
def send_image():
    serial = get_cpu_serial()


    if not os.path.exists(IMAGE_PATH):
        print("Error: Image file not found.")
        return


    with open(IMAGE_PATH, "rb") as img_file:
        encoded_image = base64.b64encode(img_file.read()).decode("utf-8")

    payload = {
        "serial": serial,
        "image": encoded_image
    }
    
    print(f"Sending request with payload: {payload}")

    try:
        response = requests.post(
            "https://diet-support.lugongdao07.workers.dev/analyze",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        print("Success:", response.json())
    except requests.exceptions.RequestException as e:
        print("Error:", e)


    os.remove(IMAGE_PATH)

    
    
    
    
def get_calorie_intakes(serial):
    url = "https://diet-support.lugongdao07.workers.dev/calorie-intakes"
    params = {"serial": serial}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        calorie_data = response.json()

        print("Calorie Intakes:")
        for item in calorie_data:
            food = item["food"]
            date = item["date"]
            calorie = item["calorie"]
            print(f"Food: {item['food']}, Date: {item['date']}, Calorie: {item['calorie']} kcal")
    
            save_calorie_data(food, date, calorie)
    
    except requests.exceptions.RequestException as e:
        print("Error retrieving calorie intake:", e)  
    
    
    

# main
def main():
    setup_gpio()
    print("start")

    while True:
        if GPIO.input(DOOR_SENSOR_PIN) == GPIO.LOW:  
            print("door opened.")
            capture_image()
            print("capture image")
            serial = get_cpu_serial()
            send_image()
            print("send image")
            get_calorie_intakes(serial)
            time.sleep(5)
            print("finish")

if __name__ == "__main__":
    main()

