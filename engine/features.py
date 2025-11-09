from playsound import playsound
import eel
import pyttsx3

# 🗣️ Text-to-Speech (Lunara’s voice)
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # female voice
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()

# 🎵 Assistant startup sound
def playAssistantSound():
    music_dir = "www\\assets\\audio\\female-vocal-321-countdown-240912.mp3"
    playsound(music_dir)

# 🎧 Click sound for mic button
@eel.expose
def playClickSound():
    music_dir = "www\\assets\\audio\\button-305770.mp3"
    playsound(music_dir)
