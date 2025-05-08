import unittest
import os
import sys
from unittest.mock import patch, MagicMock
from datetime import datetime

# Mock audio and GUI related libraries
sys.modules['pywhatkit'] = MagicMock()
sys.modules['pyautogui'] = MagicMock()
sys.modules['mouseinfo'] = MagicMock()

# Add src folder to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from assistant.main import get_ordinal, listen_wake_word, listen_for_command


class TestOrdinal(unittest.TestCase):
    def test_ordinal_numbers(self):
        self.assertEqual(get_ordinal(1), "1st")
        self.assertEqual(get_ordinal(2), "2nd")
        self.assertEqual(get_ordinal(3), "3rd")
        self.assertEqual(get_ordinal(4), "4th")
        self.assertEqual(get_ordinal(11), "11th")
        self.assertEqual(get_ordinal(21), "21st")
        self.assertEqual(get_ordinal(23), "23rd")
        self.assertEqual(get_ordinal(102), "102nd")


class TestWakeWord(unittest.TestCase):

    @patch('builtins.print')
    @patch('assistant.main.recognizer.recognize_google')
    @patch('assistant.main.recognizer.listen')
    @patch('assistant.main.sr.Microphone')
    def test_listen_wake_word(self, mock_microphone, mock_listen, mock_recognize_google, mock_print):
        mock_recognize_google.return_value = "hey Friday"
        listen_wake_word()
        mock_print.assert_any_call("listning wake word")
        mock_print.assert_any_call("You said hey Friday")


class TestListenCommand(unittest.TestCase):

    @patch('builtins.print')
    @patch('assistant.main.recognizer.recognize_google')
    @patch('assistant.main.recognizer.listen')
    @patch('assistant.main.sr.Microphone')
    def test_time_command(self, mock_microphone, mock_listen, mock_recognize_google, mock_print):
        mock_recognize_google.return_value = "time"
        listen_for_command()
        expected_time = datetime.now().strftime('%I:%M %p')
        mock_print.assert_any_call(f"The time is {expected_time}")

    @patch('builtins.print')
    @patch('assistant.main.recognizer.recognize_google')
    @patch('assistant.main.recognizer.listen')
    @patch('assistant.main.sr.Microphone')
    def test_date_command(self, mock_microphone, mock_listen, mock_recognize_google, mock_print):
        mock_recognize_google.return_value = "date"
        listen_for_command()
        today = datetime.now()
        expected_date = f"Hello! Today is {today.strftime('%A') }, the {get_ordinal(today.day)} of {today.strftime('%B')}, {today.year}."
        mock_print.assert_any_call(expected_date)


if __name__ == '__main__':
    unittest.main()
