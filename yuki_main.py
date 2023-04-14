import tempfile
import json
import sys
import openai
import time
import requests
import tkinter as tk
import os
from dotenv import load_dotenv

import simpleaudio
import speech_recognition as sr

# APIキーの設定(.envにAPIKEY,BotContentをいれてください)
load_dotenv()
openai.api_key = os.environ.get("OpenAIApikey")
BotContent = os.environ.get("BotContent")
# GUIウィンドウを生成する関数

# どう考えてもおかしいコードです(´・ω・｀)1回目の会話をカウント
count = 0
gpt_response = ""


def usegpt(text):  # ChatGPT
    global count
    global gpt_response
    if count == 0:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (BotContent)},
                {"role": "user", "content": (
                    "ご主人様が「" + text + "」と言うと、ユキはこう返した。")},
            ],
            temperature=0.7,
            max_tokens=2048,
        )
        gpt_response = response.choices[0]["message"]["content"].strip()
        count += 1
        return gpt_response
    else:  # 2回目以降
        print("2回目")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (BotContent)},
                {"role": "user", "content": (
                    "ユキが「" + text + "」と言うと、ご主人様はこう返した。")},
                {"role": "assystant", "content": (gpt_response)},
            ],
            temperature=0.7,
            max_tokens=2048,
        )
        gpt_response = response.choices[0]["message"]["content"].strip()
        return gpt_response


def Voivo(text):  # VoiceVox(VoiceVoxを起動した状態でないと動きません)
    speak_text = (("text", text), ("speaker", 16))
    send1 = requests.post(
        f"http://localhost:50021/audio_query", params=speak_text)
    send2 = requests.post(f"http://localhost:50021/synthesis", headers={
                          "Content-Type": "application/json"}, params=speak_text, data=json.dumps(send1.json()))
    with tempfile.TemporaryDirectory() as tmp:
        with open(f"{tmp}/audi.wav", "wb") as f:
            f.write(send2.content)
            sora_voice = simpleaudio.WaveObject.from_wave_file(
                f"{tmp}/audi.wav")
            waitsora = sora_voice.play()
            waitsora.wait_done()


def recog():  # SpeechRecognizer
    listener = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as source:
                print("お話してください～♪")
                voice = listener.listen(source)
                print("...")
                voice_text = listener.recognize_google(voice, language="ja-JP")
                print("あなた：「"+voice_text+"」")
                return voice_text
        except sr.UnknownValueError:
            print("聞き取れませんでした...！")
            time.sleep(3)
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))
            sys.exit()


def voice_btn():
    res1 = recog()
    voice_message(res1)
    window.update()
    res2 = usegpt(res1)
    yuki_send_message(res2)
    window.update()
    Voivo(res2)


def send_btn():
    res1 = message_entry.get()
    message_entry.delete(0, tk.END)
    voice_message(res1)
    window.update()
    res2 = usegpt(res1)
    yuki_send_message(res2)
    window.update()
    Voivo(res2)


def create_window():
    window = tk.Tk()
    window.title("AIYukiTalk")
    window.geometry("400x500")
    return window

# チャットログを表示するテキストボックスを生成する関数


def create_chat_log_textbox(window):
    chat_log_textbox = tk.Text(window)
    chat_log_textbox.place(x=10, y=10, width=380, height=400)
    return chat_log_textbox

# メッセージを入力するエントリーボックスを生成する関数


def create_message_entry(window):
    message_entry = tk.Entry(window)
    message_entry.place(x=10, y=420, width=300, height=30)
    return message_entry


def voice_message(self):
    message = self
    chat_log_textbox.insert(tk.END, "あなた: " + message + "\n")
    message_entry.delete(0, tk.END)


def yuki_send_message(self):
    message = self
    chat_log_textbox.insert(tk.END, "ユキ: " + message + "\n")


# GUIウィンドウを生成
window = create_window()

# チャットログを表示するテキストボックスを生成
chat_log_textbox = create_chat_log_textbox(window)

# メッセージを入力するエントリーボックスを生成
message_entry = create_message_entry(window)

# メッセージを送信するボタンを生成
voice_btn = tk.Button(window, text="音声！", command=voice_btn)
voice_btn.place(x=320, y=460, width=70, height=30)
send_button = tk.Button(window, text="送信", command=send_btn)
send_button.place(x=320, y=420, width=70, height=30)

window.mainloop()
