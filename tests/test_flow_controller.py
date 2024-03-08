from unittest import TestCase
from unittest.mock import MagicMock, call, patch

import phonenumbers

from source.flow_controller import BasicFlow, FlowController, formatted_phone_number, input_handler


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
    

class TestBasicFlow(TestCase):
    @patch.object(BasicFlow, "run_flow")
    def setUp(self, *_):
        self.sheet = MagicMock()
        self.controller = MagicMock()
        self.basic_flow = BasicFlow(self.sheet, self.controller)

    @patch.object(BasicFlow, "run_flow")
    def test_init(self, mock_run_flow):
        basic_flow_obj = BasicFlow(self.sheet, self.controller)
        self.assertTrue(hasattr(basic_flow_obj, "sheet"))
        self.assertTrue(hasattr(basic_flow_obj, "controller"))
        self.assertTrue(hasattr(basic_flow_obj, "info"))
        mock_run_flow.assert_called_once()
    
    def test_choose_date(self):
        date = "2020-01-01"
        
        with patch("source.flow_controller.input_handler") as mock_input_handler:
            mock_input_handler.return_value = date
            self.basic_flow.choose_date()
        
        mock_input_handler.assert_called_once()
        self.assertEqual(self.basic_flow.info["date"], date)
    
    @patch("source.flow_controller.input_handler")
    def test_choose_time(self, mock_input_handler):
        start_time = "12:00"
        duration = 1.0
        end_time = "13:00"
        self.basic_flow.info["date"] = "2024-05-05"
        self.basic_flow.info["service"] = "Test service"
        mock_time_ranges = [[start_time, end_time]]
        mock_input_handler.return_value = start_time
        self.sheet.get_service_info.return_value = duration

        self.basic_flow.choose_time(mock_time_ranges)

        mock_input_handler.assert_called_once()
        self.assertEqual(self.basic_flow.info["start_time"], start_time)
        self.assertEqual(self.basic_flow.info["end_time"], end_time)
    
    @patch.object(BasicFlow, "print_suggestion")
    @patch.object(BasicFlow, "print_options")
    @patch("source.flow_controller.input_handler")
    def test_choose_service(self, mack_input_handler, mock_print_options, mock_print_suggestion):
        test_services = [{"name": "Service 1"}, {"name": "Service 2"}]
        service_index = "0"
        self.sheet.get_services.return_value = test_services
        mack_input_handler.return_value = service_index

        self.basic_flow.choose_service("main")
        
        mack_input_handler.assert_called_once()
        mock_print_options.assert_called_once()
        mock_print_suggestion.assert_called_once()
        self.assertEqual(self.basic_flow.info["service"], test_services[int(service_index)]["name"])
    
    def test_success_message(self):
        with patch("source.flow_controller.Text") as mock_text, \
            patch("source.flow_controller.Panel") as mock_panel, \
            patch("source.flow_controller.console.print") as mock_print, \
            patch("source.flow_controller.Align.center") as mock_align, \
            patch("source.flow_controller.console.clear") as mock_clear, \
            patch("source.flow_controller.sleep") as mock_sleep:
                self.basic_flow.show_success_message("test message")
        
        self.assertEqual(mock_text.call_count, 2)
        self.assertEqual(mock_print.call_count, 2)
        self.assertEqual(mock_align.call_count, 2)
        mock_panel.assert_called_once()
        mock_clear.assert_called_once()
        mock_sleep.assert_called_once()
