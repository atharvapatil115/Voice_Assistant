import unittest
from datetime import datetime
import os
import sys
from unittest import mock
from unittest.mock import patch, MagicMock

# Mock problematic modules
sys.modules['pywhatkit'] = mock.MagicMock()
sys.modules['pyautogui'] = mock.MagicMock()
sys.modules['mouseinfo'] = mock.MagicMock()
sys.modules['pyttsx3'] = mock.MagicMock()
sys.modules['pyaudio'] = mock.MagicMock()

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from assistant.main import get_ordinal, listen_wake_word, listen_for_command

class OrdinalTest(unittest.TestCase):
    def test_for_ordinal(self):
        self.assertEqual(get_ordinal(1), "1st")
        self.assertEqual(get_ordinal(2), "2nd")
        self.assertEqual(get_ordinal(3), "3rd")
        self.assertEqual(get_ordinal(4), "4th")

class WakeWordTest(unittest.TestCase):

    @patch('builtins.print')
    @patch('assistant.main.recognizer.recognize_google', return_value="hey Friday")
    @patch('assistant.main.recognizer.listen')
    @patch('assistant.main.sr.Microphone')
    def test_for_wake_word(self, mock_microphone, mock_listen, mock_recognize_google, mock_print):
        listen_wake_word()
        mock_print.assert_any_call("listning wake word")
        mock_print.assert_any_call("You said hey Friday")

class CommandTest(unittest.TestCase):

    @patch('builtins.print')
    @patch('assistant.main.recognizer.recognize_google', return_value="time")
    @patch('assistant.main.recognizer.listen')
    @patch('assistant.main.sr.Microphone')
    def test_for_time(self, mock_microphone, mock_listen, mock_recognize_google, mock_print):
        listen_for_command()
        expected_time = datetime.now().strftime('%I:%M %p')
        mock_print.assert_any_call(f"The time is {expected_time}")

    @patch('builtins.print')
    @patch('assistant.main.recognizer.recognize_google', return_value="date")
    @patch('assistant.main.recognizer.listen')
    @patch('assistant.main.sr.Microphone')
    def test_for_date(self, mock_microphone, mock_listen, mock_recognize_google, mock_print):
        listen_for_command()
        today = datetime.now()
        expected_date = f"Hello! Today is {today.strftime('%A') }, the {get_ordinal(today.day)} of {today.strftime('%B')}, {today.year}."
        mock_print.assert_any_call(expected_date)

if __name__ == "__main__":
    unittest.main()
