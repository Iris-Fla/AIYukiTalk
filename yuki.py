import get_env
import os
import openai

# APIキーの設定
openai.api_key = (get_env.OpenAIAPI)

#
def usegpt(self):
    print("a")
    
    
    
print(usegpt.choices[0]["message"]["content"].strip())

