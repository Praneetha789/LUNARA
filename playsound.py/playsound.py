from playsound import playsound as system_sound

def playSound(music_file):
    try:
        system_sound(music_file)
    except Exception as e:
        print("Error playing sound:", e)
