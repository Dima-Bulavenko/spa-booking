from unittest import TestCase
from unittest.mock import MagicMock, call, patch

from source.flow_controller import input_handler


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
