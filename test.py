import speech_recognition  as sr
import pyttsx3 as p
from datetime import datetime
recognizer = sr.Recognizer()
import time

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
          print("listning wait word")
          audio = recognizer.listen(source)
     try:
          text = recognizer.recognize_google(audio)
          print(f"You said {text}")
          if "hey Friday" in text:
               speak("hey!, I am listening") 
               listen_for_command()
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
                    if "time" in command:
                        
                        speak(f"The time is {datetime.now().strftime('%I:%M %p')}")
                    
                    elif "date" in command:
                         today = datetime.now()
                         day = get_Ordinal(today.day)
                         month = today.strftime("%B")
                         year = today.year
                         day_of_week = today.strftime("%A")  # e.g., Wednesday
                         sentence = f"Hello! Today is {day_of_week}, the {day} of {month}, {year}."

                         speak(sentence)
                    elif "code" in command and  "addition" in command and "python" in command:
                          try:
                              with open ("addition.py","a") as f:
                                   program = "a=10 \nb=20 \nprint(f'Addition of two number is {a+b}')"
                                   f.write(program)
                                   f.close()
                              print(f"Program Created \n{program}")
                          except Exception as e:
                                print(e)
                                speak(e)
                    elif "code" in command and  "addition" in command  and "c" or "c language" in command:
                          try:
                              with open ("addition.c","a") as f:
                                   program = "#include<stdio.h> \n\nint main(){ \nint a = 10; \nint b=20; \nprintf('The addition of two numbers is %d',(a+b)); \nreturn 0; \n}"
                                   f.write(program)
                                   f.close()
                              print(f"Program Created \n{program}")
                              speak(f"Program for addition created in file addition.c")

                          except Exception as e:
                                print(e)
                                speak(e)
                    elif "shutdown" in command:
                          speak("shutting down!!")
                          start = False
                    else:
                        speak("Sorry, I didn't understand.")


        except sr.UnknownValueError:
                    speak("Sorry, I could not understand.")
        except sr.RequestError:
                    speak("Speech service error!")


# engine.say(f"Hello today's date is {datetime.now().strftime('%Y-%m-%d')}")
# engine.runAndWait()
# time.sleep(2)
# engine.say(f"is there anything else i can help you with  ??")
# engine.runAndWait()
while start:
    listen_wake_word()