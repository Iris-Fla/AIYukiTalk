import sys
import get_env
import openai
import requests
import simpleaudio
import tempfile
import json
import speech_recognition as sr

# APIキーの設定
BotContent = (get_env.BotContent)
openai.api_key = (get_env.OpenAIAPI)

# ChatGPT(.envにAPIKEY,BotContentをいれてください)


def usegpt(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": (BotContent)},
            {"role": "user", "content": (text)}
        ],
    )
    gpt_response = response.choices[0]["message"]["content"].strip()
    # print(gpt_response)
    return gpt_response
# 動作確認 usegpt("あなたの名前を教えてください。")


# VoiceVox(VoiceVoxを起動した状態でないと動きません)
def Voivo(text):
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
# 動作確認 Voivo("眠いです")


def recog():
    listener = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as source:
                print("お話してください～♪")
                voice = listener.listen(source)
                print("考え中です...!")
                voice_text = listener.recognize_google(voice, language="ja-JP")
                return voice_text
        except sr.UnknownValueError:
            print("聞き取れませんでした...")
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
