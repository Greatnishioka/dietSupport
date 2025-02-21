# カメラで庫内画像を撮影
# 画像はJPEG形式で保存
from picamera import PiCamera
from time import sleep

def capture_image():
    camera = PiCamera()
    camera.start_preview()
    sleep(2)
    image_path = "/home/pi/fridge_image.jpg"
    camera.capture(image_path)
    camera.stop_preview()
    return image_path
