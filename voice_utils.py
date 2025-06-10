# voice_utils.py
import speech_recognition as sr
import pyttsx3

def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that."
    except sr.RequestError:
        return "Sorry, voice service is unavailable."

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
