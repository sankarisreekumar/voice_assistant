import speech_recognition as sr
import datetime
import subprocess
import pywhatkit
import pyttsx3
import webbrowser

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Initialize speech recognizer
recognizer = sr.Recognizer()

def cmd():
    """Capture voice command and execute actions."""
    with sr.Microphone() as source:
        print("Clearing background noises... Please wait")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Ask me anything...")

        try:
            recorded_audio = recognizer.listen(source)
            text = recognizer.recognize_google(recorded_audio, language='en_US')
            text = text.lower()
            print("Your message:", text)

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return
        except sr.RequestError:
            print("Could not request results, check your internet connection.")
            return
        except Exception as ex:
            print("Error:", ex)
            return

    # Execute actions based on recognized text
    if "chrome" in text:
        speak_and_execute("Opening Chrome...", r"C:\Program Files\Google\Chrome\Application\chrome.exe")

    elif "time" in text:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        print("Current time:", current_time)
        engine.say(f"The time is {current_time}")
        engine.runAndWait()

    elif "play" in text:
        engine.say("Opening YouTube to play the requested video.")
        engine.runAndWait()
        song = text.replace("play", "").strip()
        pywhatkit.playonyt(song)

    elif "youtube" in text:
        speak_and_execute("Opening YouTube", "https://www.youtube.com")

    elif "exit" in text or "stop" in text:
        engine.say("Goodbye!")
        engine.runAndWait()
        exit()

    else:
        engine.say("I didn't understand that command.")
        engine.runAndWait()

def speak_and_execute(message, command):
    """Helper function to speak a message and execute a command."""
    engine.say(message)
    engine.runAndWait()
    if command.startswith("http"):
        webbrowser.open(command)
    else:
        subprocess.Popen([command])

# Run in a loop
while True:
    cmd()
