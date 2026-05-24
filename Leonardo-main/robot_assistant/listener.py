import speech_recognition as sr

recognizer = sr.Recognizer()

def listen():
    try:
        # device_index=1 is required for your USB microphone!
        with sr.Microphone(device_index=1) as source:
            print(">> Ακούω... (Μίλα τώρα)")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)

        text = recognizer.recognize_google(audio, language="el-GR")
        print(">> Είπες:", text)
        return text.lower()

    except Exception as e:
        # This prevents the program from crashing if it hears nothing
        return ""
