import speech_recognition as sr
import pyttsx3
import datetime
import time
import threading

# === Speak function (guaranteed voice output) ===
def speak(text):
    import pyttsx3
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 170)
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# === Listen to user command ===
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except Exception:
        print("Sorry, I didn’t catch that. Please repeat.")
        return ""
    return query.lower()

# === Get current date and time ===
def tell_date_time():
    now = datetime.datetime.now()
    date_str = now.strftime("%B %d, %Y")
    time_str = now.strftime("%I:%M %p")
    speak(f"Today's date is {date_str} and the time is {time_str}")

# === Reminder functionality ===
reminders = []

def add_reminder(task, remind_time):
    reminders.append((task, remind_time))
    speak(f"Reminder added for {task} at {remind_time.strftime('%I:%M %p')}")

def check_reminders():
    while True:
        now = datetime.datetime.now().replace(second=0, microsecond=0)
        for task, t in reminders.copy():
            if t == now:
                speak(f"Reminder! It's time to {task}")
                reminders.remove((task, t))
        time.sleep(20)

# === Main assistant ===
def main():
    speak("Hello Nishi, this is your voice assistant.")
    threading.Thread(target=check_reminders, daemon=True).start()

    while True:
        query = take_command()

        if 'time' in query:
            tell_date_time()

        elif 'date' in query:
            tell_date_time()

        elif 'reminder' in query:
            speak("What should I remind you about?")
            task = take_command()

            speak("At what hour should I remind you?")
            hour_str = take_command()
            speak("And what minute?")
            minute_str = take_command()

            try:
                hour = int(hour_str)
                minute = int(minute_str)
                now = datetime.datetime.now()
                remind_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                add_reminder(task, remind_time)
            except:
                speak("Sorry, I couldn’t understand the time.")

        elif 'exit' in query or 'stop' in query or 'bye' in query:
            speak("Goodbye Nishi! Have a great day.")
            break

        elif query == "":
            continue

        else:
            speak("Sorry, I didn’t understand that.")

if __name__ == "__main__":
    main()
