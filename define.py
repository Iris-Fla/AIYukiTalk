import get_env
import openai
import requests, simpleaudio, tempfile, json

# APIキーの設定
BotContent = (get_env.BotContent)
openai.api_key = (get_env.OpenAIAPI)

#ChatGPT(.envにAPIKEY,BotContentをいれてください)
def usegpt(self):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": (BotContent)},
        {"role": "user", "content": (self)}
        ],
    )
    print(response.choices[0]["message"]["content"].strip())
    
#動作確認 usegpt("あなたの名前を教えてください。")


#VoiceVox(VoiceVoxを起動した状態でないと動きません)
def zundamon(self):
    localhost = "127.0.0.1"
    port = 50021
    speak_text = (("text",self),("speaker", 15))
    send1 = requests.post(f"http://{localhost}:{port}/audio_query",params=speak_text)
    send2 = requests.post(f"http://{localhost}:{port}/synthesis",headers={"Content-Type": "application/json"},params=speak_text,data=json.dumps(send1.json()))

    with tempfile.TemporaryDirectory() as tmp:
        with open(f"{tmp}/audi.wav", "wb") as f:
            f.write(send2.content)
            sora_voice = simpleaudio.WaveObject.from_wave_file(f"{tmp}/audi.wav")
            waitsora = sora_voice.play()
            waitsora.wait_done()

#動作確認 zundamon("眠いです")

