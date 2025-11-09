import speech_recognition as sr
import pyttsx3
import eel
import time
import webbrowser
import pywhatkit
import os
import openai
from dotenv import load_dotenv

# ✅ Load .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

eel.init('www')

# 🎙 Voice setup
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 165)
engine.setProperty('volume', 0.9)

def speak(text):
    print(f"Lunara 🩵: {text}")
    eel.show_text(text)
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.5)  # wait before listening again

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        eel.show_text("🎧 Listening...")
        print("🎧 Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=8, phrase_time_limit=6)

    try:
        eel.show_text("🧠 Recognizing...")
        print("🧠 Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"🪶 You said: {query}")
        eel.show_text(f"You said: {query}")
        return query.lower()
    except Exception:
        eel.show_text("Sorry, could you say that again? 🥺")
        return ""

@eel.expose
def start_lunara():
    speak("Hey Praneetha! I'm Lunara, your personal AI assistant 💫")
    while True:
        query = take_command()

        if query == "":
            continue

        # 🌐 Websites & Apps
        if 'open youtube' in query:
            speak("Opening YouTube for you 🎬")
            webbrowser.open("https://www.youtube.com")

        elif 'play' in query:
            song = query.replace('play', '')
            speak(f"Playing {song} 🎵")
            pywhatkit.playonyt(song)

        elif 'open chrome' in query:
            speak("Opening Google Chrome 🌍")
            os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")

        elif 'open notepad' in query:
            speak("Opening Notepad 📘")
            os.system("notepad")

        elif 'time' in query:
            strTime = time.strftime("%I:%M %p")
            speak(f"The time is {strTime}")

        elif 'exit' in query or 'quit' in query or 'stop' in query:
            speak("Goodbye, Praneetha! Talk to you soon 💙")
            break

        # 🧠 Smart response using OpenAI
        else:
            try:
                eel.show_text("💭 Thinking...")
                print("💭 Thinking...")
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are Lunara, a caring, lively AI who speaks warmly with Praneetha."},
                        {"role": "user", "content": query}
                    ]
                )
                reply = response["choices"][0]["message"]["content"].strip()
                speak(reply)
            except Exception as e:
                speak("Hmm... my connection to the brain is a bit fuzzy right now 🧠💤")

eel.start('index.html', size=(900, 600))
