import requests

# 音声合成のリクエストを送信するURL
url = "http://localhost:50021/api/synthesis"

# 音声合成のパラメーター
params = {
    "text": "こんにちは、Voicevox REST APIです。",
    "speaker": "show",
    "speed": 1.5,
    "volume": 1.0,
    "pitch": 1.0,
    "range": 1.0
}

# 音声合成のリクエストを送信する
response = requests.post(url, json=params)

# 音声をファイルに保存する
with open("output.wav", "wb") as f:
    f.write(response.content)
