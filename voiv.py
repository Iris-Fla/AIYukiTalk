import json
import requests
import tempfile
import simpleaudio


def Voivo(text):  # VoiceVox(VoiceVoxを起動した状態でないと動きません)
    speak_text = (("text", text), ("speaker", 0))
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


Voivo("こんにちは")
