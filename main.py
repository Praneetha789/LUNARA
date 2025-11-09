import eel
import speech_recognition as sr
import pyttsx3
from openai import OpenAI
import os
from dotenv import load_dotenv
import time
import webbrowser

# ---------------------- SETUP ----------------------
eel.init("www")  # Folder name for frontend

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in .env file!")

client = OpenAI(api_key=api_key)

engine = pyttsx3.init()
engine.setProperty("rate", 175)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # female voice

def speak(text):
    print(f"Lunara 🩵: {text}")
    engine.say(text)
    engine.runAndWait()

# ---------------------- OPENAI CHAT ----------------------
def ask_openai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # ✅ More stable & latest small GPT-4 model
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message.content
        return reply
    except Exception as e:
        print("Error:", e)
        return "Sorry, I had trouble connecting to OpenAI."

# ---------------------- VOICE RECOGNITION ----------------------
def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("🎧 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("🧠 Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"🪶 You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return "network error"

# ---------------------- COMMANDS ----------------------
def process_command(command):
    if "open youtube" in command:
        speak("Opening YouTube 🎬")
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube 🎬"

    elif "open chrome" in command:
        speak("Opening Chrome 🌐")
        os.system("start chrome")
        return "Opening Chrome 🌐"

    elif "open notepad" in command:
        speak("Opening Notepad 📄")
        os.system("notepad")
        return "Opening Notepad 📄"

    elif "open whatsapp" in command:
        speak("Opening WhatsApp 💬")
        webbrowser.open("https://web.whatsapp.com")
        return "Opening WhatsApp 💬"

    elif command.strip() == "":
        return "I didn’t catch that, could you repeat?"

    else:
        reply = ask_openai(command)
        speak(reply)
        return reply

# ---------------------- EEL EXPOSED FUNCTION ----------------------
@eel.expose
def start_lunara():
    speak("Hey Praneetha! I'm Lunara, your personal AI assistant 💫")
    while True:
        command = listen()
        response = process_command(command)
        eel.show_text(response)
        time.sleep(1)

# ---------------------- START APP ----------------------
if __name__ == "__main__":
    eel.start("index.html", size=(900, 600))
