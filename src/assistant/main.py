import speech_recognition  as sr
import pyttsx3 as p
import datetime 
recognizer = sr.Recognizer()
import time
import os
import webbrowser
import pyjokes
from preprocessing.Vectorization import Calculate_best_match
global start
start = True
def get_Ordinal(n):
      if 10<= n%100  <=20:
            suffix = 'th'
      else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
      return f"{n}{suffix}"
def speak(text):
    engine = p.init()

    voices = engine.getProperty('voices')


    for voice in voices:
        if "Microsoft Hazel Desktop" in voice.name:
                engine.setProperty('voice',voice.id)
                break
    engine.setProperty('rate',140)
    engine.setProperty('volume',0.9)

    engine.say(text)
    engine.runAndWait()

# with sr.Microphone() as source:
#     print("say something")
#     audio = recognizer.listen(source)
#     text = recognizer.recognize_google(audio)
#     print(f"You said: \t {text}")

def listen_wake_word():
     with sr.Microphone() as source:
          print("listning wake word")
          audio = recognizer.listen(source)
     try:
          text = recognizer.recognize_google(audio)
          print(f"You said {text}")
          if "Friday" in text:
               speak("hey!, I'm listning") 
               listen_for_command()
          else:
                speak("sorry wrong wake word")
     except sr.UnknownValueError:
          pass
     except sr.RequestError:
          print("error in connection")

def listen_for_command():
        with sr.Microphone() as source:
          print("listning for command")
          audio = recognizer.listen(source)
        try:
                    command = recognizer.recognize_google(audio).lower()
                    print(f"Command received: {command}")
                    # You can add your command handling here
                    action_name,score = Calculate_best_match(command)
                    if action_name:
                          action_function = globals().get(action_name)
                          if action_function:
                                action_function()
                          else:
                                speak("Sorry, I know what you mean, but I don't know how to do it yet.")

                    else:
                        speak("Sorry, I didn't understand that.")

        except sr.UnknownValueError:
                    speak("Sorry, I could not understand.")
        except sr.RequestError:
                    speak("Speech service error!")


# engine.say(f"Hello today's date is {datetime.datetime.now().strftime('%Y-%m-%d')}")
# engine.runAndWait()
# time.sleep(2)
# engine.say(f"is there anything else i can help you with  ??")
# engine.runAndWait()

def launch_browser():
    speak("Opening browser")
    webbrowser.open("https://www.google.com")

def tell_time():
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    speak(f"The time is {current_time}")

def say_joke():
     speak("DO you really wanna hear a joke?")
     with sr.Microphone() as source:
          audio = recognizer.listen(source)
          answer = recognizer.recognize_google(audio).lower()
          print(f"Command received: {answer}")
     if "yes" in answer :
           joke = pyjokes.get_joke()
           speak(joke)

     else:
          speak("opration cancelled!")
   
def shutdown_system():
    
     speak("DO you really want to shutdown system??")
     with sr.Microphone() as source:
          audio = recognizer.listen(source)
          answer = recognizer.recognize_google(audio).lower()
          print(f"Command received: {answer}")
     if "yes" in answer :
          speak("Shutting down the system")
          os.system("shutdown /s /t 1")
     else:
          speak("opration cancelled!")

# def play_music():
#     speak("Playing music")
#     os.startfile("C:\\Path\\To\\Your\\Music.mp3")  

def tell_date():
    today = datetime.datetime.now()
    day = get_Ordinal(today.day)
    month = today.strftime("%B")
    year = today.year
    day_of_week = today.strftime("%A")
    sentence = f"Today is {day_of_week}, the {day} of {month}, {year}."
    speak(sentence)

if __name__ == "__main__":
     speak("Hello there! System started")
     speak("Say the wake word")
     while start:
            listen_wake_word()