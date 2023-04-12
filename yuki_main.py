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


def create_window():
    window = tk.Tk()
    window.title("チャットアプリ")
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

# メッセージを送信するボタンを生成する関数


def create_send_button(window, message_entry, chat_log_textbox):
    def send_message():
        message = message_entry.get()
        chat_log_textbox.insert(tk.END, "You: " + message + "\n")
        message_entry.delete(0, tk.END)
    send_button = tk.Button(window, text="送信", command=send_message)
    send_button.place(x=320, y=420, width=70, height=30)
    return send_button


# GUIウィンドウを生成
window = create_window()

# チャットログを表示するテキストボックスを生成
chat_log_textbox = create_chat_log_textbox(window)

# メッセージを入力するエントリーボックスを生成
message_entry = create_message_entry(window)

# メッセージを送信するボタンを生成
send_button = create_send_button(window, message_entry, chat_log_textbox)


def usegpt(text):  # ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": (BotContent)},
            {"role": "user", "content": (text)}
        ],
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
                return voice_text
        except sr.UnknownValueError:
            print("聞き取れませんでした...！")
            time.sleep(3)
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))
            sys.exit()
# 動作確認 recog()


def yukigpt():
    recog_return = recog()
    print("あなた「"+recog_return+"」")
    gpt_rep = usegpt(recog_return)
    print("ユキ「"+(gpt_rep)+"」")
    Voivo(gpt_rep)


yukigpt()
