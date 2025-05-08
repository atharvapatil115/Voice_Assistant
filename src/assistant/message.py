import webbrowser
import pyautogui
import time

def send_Message(number, message):
    url = f"https://wa.me/{number}?text={message}"
    webbrowser.open(url)
    time.sleep(10)  # wait for the page and WhatsApp Web to load

    pyautogui.press("enter")  # sends the message
