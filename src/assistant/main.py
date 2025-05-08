import speech_recognition as sr
import pyttsx3 as p
import datetime
import os
import pywhatkit
import webbrowser
import pyjokes
from difflib import get_close_matches
from preprocessing.Vectorization import Calculate_best_match
from Utils.Data_Logger import log_info, log_error, log_warning
import sys
from .message import send_Message
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Initialize
recognizer = sr.Recognizer()
start = True
contacts = {
    "samiksha": "+917397856907",
    "atharva": "+919322392155",
    "atharv": "+919322392155",
    "sahil" : "+919175750198"
}

# Text-to-speech engine
engine = p.init()
engine.setProperty('rate', 140)
engine.setProperty('volume', 0.9)
for voice in engine.getProperty('voices'):
    if "Microsoft Hazel Desktop" in voice.name:
        engine.setProperty('voice', voice.id)
        break

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

def get_best_contact_match(spoken_name, contacts):
    matches = get_close_matches(spoken_name, contacts.keys(), n=1, cutoff=0.7)
    return matches[0] if matches else None

# Voice Assistant Functions
def launch_browser():
    speak("Opening browser")
    webbrowser.open("https://www.google.com")

def tell_time():
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    speak(f"The time is {current_time}")

def tell_date():
    today = datetime.datetime.now()
    day = get_ordinal(today.day)
    month = today.strftime("%B")
    year = today.year
    day_of_week = today.strftime("%A")
    speak(f"Today is {day_of_week}, the {day} of {month}, {year}.")

def say_joke():
    while True:
        speak("Do you want to hear a joke?")
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        try:
            answer = recognizer.recognize_google(audio).lower()
            if "yes" in answer:
                speak(pyjokes.get_joke())
                return
            elif "exit" in answer:
                speak("Cancelling joke.")
                return
            else:
                speak("Operation cancelled.")
                return
        except:
            speak("Sorry, I didn't catch that. Please say again or say 'exit' to cancel.")

def shutdown_system():
    while True:
        speak("Do you really want to shut down the system?")
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        try:
            answer = recognizer.recognize_google(audio).lower()
            if "yes" in answer:
                speak("Shutting down the system")
                os.system("shutdown /s /t 1")
                return
            elif "exit" in answer:
                speak("Cancelling shutdown.")
                return
            else:
                speak("Operation cancelled.")
                return
        except:
            speak("Didn't catch that. Please repeat or say 'exit' to cancel.")

def sendMessage():
    global contacts
    while True:
        speak("To whom do you want to send the message?")
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        try:
            contact_name = recognizer.recognize_google(audio).lower()
            log_info(f"You Said: {contact_name}")
            if contact_name == "exit":
                speak("Cancelling message.")
                return
            best_match = get_best_contact_match(contact_name, contacts)
        except:
            speak("Sorry, I couldn't understand the name. Please try again or say 'exit'.")
            continue

        if best_match:
            contact_name = best_match

        if contact_name in contacts:
            speak("What message do you want to send?")
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
            try:
                message = recognizer.recognize_google(audio).lower()
                if "exit" in message:
                    speak("Cancelling message.")
                    return
                log_info(f"Message: {message}")
                speak(f"Your message is: {message}")
                speak(f"Do you want to send it to {contact_name}?")
                with sr.Microphone() as source:
                    audio = recognizer.listen(source)
                ans = recognizer.recognize_google(audio).lower()
                if "send" in ans:
                    # pywhatkit.sendwhatmsg_instantly(contacts[contact_name], message)
                    send_Message(message,contacts[contact_name])
                    speak("Message sent successfully.")
                    return
                else:
                    speak("Message cancelled.")
                    return
            except:
                speak("Couldn't process the message. Try again or say 'exit'.")
        else:
            speak(f"The contact {contact_name} is not in the contact list. Add new?")
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
            try:
                ans = recognizer.recognize_google(audio).lower()
                if "yes" in ans:
                    speak("What is the name of the contact?")
                    with sr.Microphone() as source:
                        name_audio = recognizer.listen(source)
                    name_of_contact = recognizer.recognize_google(name_audio).lower()
                    speak("What is the phone number?")
                    with sr.Microphone() as source:
                        number_audio = recognizer.listen(source)
                    spoken_number = recognizer.recognize_google(number_audio).lower()

                    def convert_spoken_number(spoken):
                        word_to_digit = {
                            "zero": "0", "one": "1", "two": "2", "three": "3",
                            "four": "4", "five": "5", "six": "6",
                            "seven": "7", "eight": "8", "nine": "9"
                        }
                        return "+91" + "".join([word_to_digit.get(w, "") for w in spoken.split()])

                    number = convert_spoken_number(spoken_number)
                    if len(number) == 13:
                        contacts[name_of_contact] = number
                        speak(f"{name_of_contact} added to contacts.")
                    else:
                        speak("Phone number format seems incorrect.")
                else:
                    speak("Contact not added.")
            except:
                speak("Couldn't complete contact addition. Please try again.")

def listen_for_command():
    while True:
        with sr.Microphone() as source:
            print("Listening for command...")
            audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"Command received: {command}")
            if "exit" in command:
                speak("Cancelling current command.")
                return
            action_name, score = Calculate_best_match(command)
            if action_name:
                action_function = globals().get(action_name)
                if action_function:
                    action_function()
                    return
                else:
                    speak("I know what you mean, but I don't know how to do that yet.")
            else:
                speak("Sorry, I didn't understand that.")
        except sr.UnknownValueError:
            speak("Sorry, I could not understand. Please repeat or say 'exit'.")
        except sr.RequestError:
            speak("Speech service error!")

def listen_wake_word():
    global start
    with sr.Microphone() as source:
        print("Listening for wake word...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio).lower()
        print(f"You said: {text}")
        if "friday" in text:
            speak("Hey! I'm listening.")
            listen_for_command()
        elif "exit" in text or "shutdown friday" in text:
            speak("Goodbye!")
            start = False
        else:
            speak("Wrong wake word.")
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        speak("Connection error.")

# Main
if __name__ == "__main__":
    # print(contacts["atharva"])
    speak("Hello there! System started.")
    log_info("System has started")
    speak("Say the wake word.")
    while start:
        listen_wake_word()
