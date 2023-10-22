from gtts import gTTS
import os

filename = "speech.mp3"
def text_to_speech(text):
    tts = gTTS(text=text, lang='fr')
    filename = "sounds/speech.mp3"
    tts.save(filename)

if __name__ == "__main__":
    text = "La team Sebastien est la meilleure!"
    text_to_speech(text)
    

