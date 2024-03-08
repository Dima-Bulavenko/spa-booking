from unittest import TestCase
from unittest.mock import MagicMock, call, patch

import phonenumbers

from source.flow_controller import FlowController, formatted_phone_number, input_handler


class InputHandler(TestCase):
    @patch("source.flow_controller.console.input")
    @patch("source.flow_controller.console.print")
    def test_valid_input(self, mock_print, mock_input):
        data = "Valid input"
        prompt_message = "Prompt message"
        mock_validator = MagicMock(return_value=None)
        mock_input.return_value = data
        result = input_handler(prompt_message, mock_validator)

        mock_validator.assert_called_once_with(data)
        mock_print.assert_not_called()
        self.assertEqual(result, data)
    
    @patch("source.flow_controller.console.input")
    def test_invalid_input(self, mock_input):
        data = "valid input"
        invalid_data = "invalid input"
        prompt_message = "prompt message"
        exception_message = "your input is invalid"
        mock_validator = MagicMock(side_effect=[ValueError(exception_message), None])
        mock_input.side_effect = [invalid_data, data]
        result = input_handler(prompt_message, mock_validator)

        mock_validator.assert_has_calls([call(invalid_data), call(data)])
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


class TestFlowController(TestCase):

    @patch.object(FlowController, "manage_options")
    @patch.object(FlowController, "print_suggestion")
    def setUp(self, *_):
        self.sheet = MagicMock()
        self.flow_controller = FlowController(self.sheet)
    
    @patch.object(FlowController, "manage_options")
    @patch.object(FlowController, "print_suggestion")
    def test_init(self, mock_print_suggestion, mock_manage_options):
        mock_sheet = MagicMock()
        controller_obj = FlowController(mock_sheet)

        self.assertTrue(hasattr(controller_obj, "sheet"))
        mock_print_suggestion.assert_called_once()
        mock_manage_options.assert_called_once()
    
    @patch.object(FlowController, "create_flow")
    @patch("source.flow_controller.input_handler")
    @patch.object(FlowController, "print_suggestion")
    @patch.object(FlowController, "print_options")
    def test_menage_options(self,
                            mock_print_options,
                            mock_print_suggestion,
                            mock_input_handler,
                            mock_create_flow):
        input_value = "0"
        mock_input_handler.return_value = input_value
        mock_create_flow.side_effect = StopIteration
        with self.assertRaises(StopIteration):
            self.flow_controller.manage_options()
        
        mock_print_options.assert_called_once()
        mock_print_suggestion.assert_called_once()
        mock_input_handler.assert_called_once()
        mock_create_flow.assert_called_once_with(input_value)

    def test_create_flow(self):
        flow_index = "0"

        with patch.object(FlowController, "FLOW_OPTIONS", new=[{"object": MagicMock()}]) as list_mock:
            self.flow_controller.create_flow(flow_index)
        
        list_mock[int(flow_index)]["object"].assert_called_once_with(self.flow_controller.sheet, self.flow_controller)
    
    
