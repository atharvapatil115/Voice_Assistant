import unittest 
from datetime import datetime
import os
from unittest.mock import patch
import sys
from unittest import mock

sys.modules['pywhatkit'] = mock.MagicMock()
sys.modules['pyautogui'] = mock.MagicMock()
sys.modules['mouseinfo'] = mock.MagicMock()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from assistant.main import get_ordinal, listen_wake_word,listen_for_command

class Ordinal_test(unittest.TestCase):
    def test_for_ordinal1(self):
        self.assertEqual(get_Ordinal(1), "1st")
        self.assertEqual(get_Ordinal(2), "2nd")
        self.assertEqual(get_Ordinal(3), "3rd")
        self.assertEqual(get_Ordinal(4), "4th")

class Wake_word_test(unittest.TestCase):

    @patch('builtins.print')
    @patch('assistant.main.recognizer.recognize_google')  # Correct patch path
    @patch('assistant.main.recognizer.listen')             # Correct patch path
    @patch('assistant.main.sr.Microphone')                 # Mock microphone
    def test_for_WakeWord(self, mock_microphone, mock_listen, mock_recognize_google, mocked_print):
        mock_recognize_google.return_value = "hey Friday"
        
        listen_wake_word()

        mocked_print.assert_any_call("listning wake word")
        mocked_print.assert_any_call("You said hey Friday")

# class Command_test(unittest.TestCase):

#     @patch('builtins.print')
#     @patch('assistant.main.recognizer.recognize_google')  # Correct patch path
#     @patch('assistant.main.recognizer.listen')             # Correct patch path
#     @patch('assistant.main.sr.Microphone')                 # Mock microphone
#     def test_for_time(self, mock_microphone, mock_listen, mock_recognize_google, mocked_print):
#         mock_recognize_google.return_value = "time"
        
#         listen_for_command()

#         mocked_print.assert_any_call(f"The time is {datetime.now().strftime('%I:%M %p')}")
#         # mocked_print.assert_any_call("You said hey Friday")
    
#     @patch('builtins.print')
#     @patch('assistant.main.recognizer.recognize_google') 
#     @patch('assistant.main.recognizer.listen')             #
#     @patch('assistant.main.sr.Microphone')      
#     def test_for_date(self,mock_microphone, mock_listen, mock_recognize_google,mocked_print):
#         mock_recognize_google.return_value = "date"
#         listen_for_command()

#         mocked_print.assert_any_call(f"Hello! Today is {datetime.now().strftime('%A') }, the {get_Ordinal(datetime.now().day)} of {datetime.now().strftime('%B')}, {datetime.now().year}.")
