# -*- coding: utf-8 -*-
import os
from gtts import gTTS

def speak(text):
    print("Robot:", text)
    tts = gTTS(text=text, lang='el')
    tts.save("voice.mp3")
    
    # Χρήση του pulse audio για το Bluetooth ηχείο
    os.system("mpg123 -q -a pulse voice.mp3")
