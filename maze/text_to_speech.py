from gtts import gTTS


def text_to_speech(text, path: str):
    assert path.endswith(".mp3")
    tts = gTTS(text=text, lang='fr')
    filename = path
    tts.save(filename)


if __name__ == "__main__":
    text = "La team Sebastien est la meilleure!"
    text_to_speech(text)
