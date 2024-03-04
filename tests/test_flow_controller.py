from unittest import TestCase
from unittest.mock import MagicMock, call, patch

import phonenumbers

from source.flow_controller import formatted_phone_number, input_handler


@patch("source.flow_controller.input")
@patch("source.flow_controller.print")
class InputHandler(TestCase):
    def test_valid_input(self, mock_print, mock_input):
        data = "Valid input"
        prompt_message = "Prompt message"
        mock_validator = MagicMock(return_value=None)
        mock_input.return_value = data
        result = input_handler(prompt_message, mock_validator)

        mock_input.assert_called_once_with(prompt_message + "\n")
        mock_validator.assert_called_once_with(data)
        mock_print.assert_not_called()
        self.assertEqual(result, data)
    
    def test_invalid_input(self, mock_print, mock_input):
        data = "valid input"
        invalid_data = "invalid input"
        prompt_message = "prompt message"
        exception_message = "your input is invalid"
        mock_validator = MagicMock(side_effect=[ValueError(exception_message), None])
        mock_input.side_effect = [invalid_data, data]
        result = input_handler(prompt_message, mock_validator)

        mock_input.assert_has_calls([call(f"{prompt_message}\n"), call(f"{prompt_message}\n")])
        mock_validator.assert_has_calls([call(invalid_data), call(data)])
        mock_print.assert_called_once_with(f"Invalid input: {exception_message}")
        self.assertEqual(result, data)


class FormattedPhoneNumber(TestCase):
    def test_valid_phone_number(self):
        phone_number = "+359 123456789"
        result = formatted_phone_number(phone_number)
        self.assertEqual(result, "+359123456789")

    def test_invalid_phone_number(self):
        phone_number = "359 123456789"
        with self.assertRaises(phonenumbers.phonenumberutil.NumberParseException) as err:
            formatted_phone_number(phone_number)
        self.assertEqual(str(err.exception), "(0) Missing or invalid default region.")
