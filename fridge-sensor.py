#  冷蔵庫を開けた時に写真を撮影して、バックエンドに送信する
#  画像を送信後は削除する
#  センサーで扉開閉を検知

import cv2
import requests
import os
from datetime import datetime
import RPi.GPIO as GPIO
from picamera import PiCamera
import time

BACKEND_URL = "https://your-vercel-backend-url.com"
IMAGE_PATH = "/home/pi/fridge_image.jpg"
DOOR_SENSOR_PIN = 18

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def capture_image():
    camera = PiCamera()
    time.sleep(2)  # カメラ起動待機
    camera.capture(IMAGE_PATH)
    camera.close()

def send_image():
    with open(IMAGE_PATH, 'rb') as img:
        files = {'image': img}
        response = requests.post(f"{BACKEND_URL}/api/fridge-content", files=files)
        print(response.json())
    os.remove(IMAGE_PATH)

def main():
    setup_gpio()
    while True:
        if GPIO.input(DOOR_SENSOR_PIN) == GPIO.LOW:  # 扉が開いた
            print(" door opened")
            capture_image()
            send_image()
            time.sleep(5)  # 誤作動防止

if __name__ == "__main__":
    main()
