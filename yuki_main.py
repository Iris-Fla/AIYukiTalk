import get_env
import openai
import requests, simpleaudio, tempfile, json
import speech_recognition as sr

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
    gpt_response = response.choices[0]["message"]["content"].strip()
    #print(gpt_response)
    return gpt_response
#動作確認 usegpt("あなたの名前を教えてください。")


#VoiceVox(VoiceVoxを起動した状態でないと動きません)
def Voivo(self):
    speak_text = (("text",self),("speaker", 15))
    send1 = requests.post(f"http://localhost:50021/audio_query",params=speak_text)
    send2 = requests.post(f"http://localhost:50021/synthesis",headers={"Content-Type": "application/json"},params=speak_text,data=json.dumps(send1.json()))

    with tempfile.TemporaryDirectory() as tmp:
        with open(f"{tmp}/audi.wav", "wb") as f:
            f.write(send2.content)
            sora_voice = simpleaudio.WaveObject.from_wave_file(f"{tmp}/audi.wav")
            waitsora = sora_voice.play()
            waitsora.wait_done()
#動作確認 Voivo("眠いです")

def recog():
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("...")
            voice = listener.listen(source)
            voice_text = listener.recognize_google(voice, language="ja-JP")
            print("あなた「"+voice_text+"」")
            return voice_text
    except sr.UnknownValueError:
        print("could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
#動作確認 recog()

def main():
    recog_return = recog()
    gpt_rep =usegpt(recog_return)
    Voivo(gpt_rep)
    print("ユキ「"+(gpt_rep)+"」")
main()