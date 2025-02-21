# ユーザー登録関連処理


import requests

def get_serial():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('Serial'):
                    return line.split(':')[1].strip()
    except Exception as e:
        return None

def register_user():
    user_data = {
        "userData": {
            "name": "hogehoge",
            "nameKana": "hogehoge",
            "bodyData": {
                "age": 30,
                "weight": 70,
                "height": 170,
                "bodyFatPercentage": 20,
                "gender": 1
            },
            "lifeCycle": {
                "wakeUpTime": "07:00",
                "sleepTime": "23:00"
            },
            "likes": {
                "likeFoods": ["hoge1", "hoge2"],
                "likeHobbies": ["hoge3", "hoge4"]
            }, 
            #今日取得していくカロリーを保持。冷蔵庫の中身を見て、カロリーを加算していく
            "todayCalories": 0

        },
        "deviceData": {
            "cpuSerialNumber": get_serial()
        }
    }

    response = requests.post("https://diet-support.lugongdao07.workers.dev/register", json=user_data)
    if response.status_code == 200:
        print("user registration successful")
    else:
        print("registration failed")

if __name__ == "__main__":
    register_user()
