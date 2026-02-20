import sounddevice as sd
import vosk
import json
import os
import pyttsx3
import datetime
import time

# ---------------- CONFIG ----------------
MODEL_PATH = "vosk-model-small-hi-0.22"  # Put the Hindi Vosk model folder here
SAMPLE_RATE = 16000

if not os.path.exists(MODEL_PATH):
    print("Model not found! Download from https://alphacephei.com/vosk/models and unzip.")
    exit()

# ---------------- LOAD MODEL ----------------
model = vosk.Model(MODEL_PATH)
recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)

# ---------------- TTS ----------------
def speak(text):
    print("Assistant:", text)
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        del engine
        time.sleep(0.3)
    except Exception as e:
        print("Voice error:", e)

# ---------------- COMMANDS ----------------
last_response = ""

def execute_command(cmd):
    global last_response
    now = datetime.datetime.now()

    if cmd == "नमस्ते":
        last_response = "Namaste! Main aapki madad ke liye hoon"
    elif cmd == "समय":
        last_response = f"Samay hai {now.strftime('%H:%M')}"
    elif cmd == "तारीख":
        last_response = f"Aaj ki tarikh {now.strftime('%d %B %Y')}"
    elif cmd == "नाम":
        last_response = "Mera naam Hindi Assistant hai"
    elif cmd == "मौसम":
        last_response = "Aaj ka mausam normal hai"
    elif cmd == "धन्यवाद":
        last_response = "Aapka swagat hai"
    elif cmd == "मदद":
        last_response = "Aap samay, tarikh, mausam, naam, joke pooch sakte hain"
    elif cmd == "चुटकुला":
        last_response = "Programmer ne chhutti kyun li? Cache clear karna tha!"
    elif cmd == "कैसे हो":
        last_response = "Main bilkul theek hoon"
    elif cmd == "फिर बोलो":
        last_response = last_response if last_response else "Kuch dohrane ko nahi hai"
    elif cmd == "दिन":
        last_response = f"Aaj {now.strftime('%A')} hai"
    elif cmd == "साल":
        last_response = f"Saal {now.strftime('%Y')}"
    elif cmd == "किसने बनाया":
        last_response = "Mujhe aapke project ke liye banaya gaya hai"
    elif cmd == "तुम कौन":
        last_response = "Main ek offline Hindi voice assistant hoon"
    elif cmd in ["अलविदा", "बंद"]:
        last_response = "Alvida! Phir milenge"
    else:
        last_response = "Maaf kijiye, main samajh nahi paayi"

    speak(last_response)
    return cmd in ["अलविदा", "बंद"]

# ---------------- LISTEN FUNCTION ----------------
def listen():
    print("\n🎤 Bol Hindi mein (microphone)...")
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16', channels=1) as stream:
        while True:
            data, _ = stream.read(4000)
            if recognizer.AcceptWaveform(bytes(data)):
                result = json.loads(recognizer.Result())
                recognizer.Reset()
                text = result.get("text", "")
                if text:
                    print("You said:", text)
                    return text

# ---------------- MAIN LOOP ----------------
speak("Hindi voice assistant shuru ho gaya hai")

while True:
    command_text = listen()
    stop = execute_command(command_text)
    if stop:
        break