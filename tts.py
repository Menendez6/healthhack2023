from gtts import gTTS
import os

filename = "speech.mp3"
def text_to_speech(text):
    tts = gTTS(text=text, lang='fr')
    filename = "speech.mp3"
    tts.save(filename)
    os.system("play " + filename +" tempo 1.25")

if __name__ == "__main__":
    text = "La team Sebastien est la meilleure!"
    text_to_speech(text)
    

