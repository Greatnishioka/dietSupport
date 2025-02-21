# 起動ファイル

from user_registration import register_user
from fridge_sensor import monitor_fridge
from api_client import send_fridge_data

if __name__ == "__main__":
    register_user()       # 初回だけ呼ばれる
    monitor_fridge()  