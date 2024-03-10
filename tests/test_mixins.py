from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

from source.mixins import PrintMixin


@patch("source.mixins.console.print")
class TestPrintMixin(TestCase):
    def setUp(self, *_):
        self.print_mixin = PrintMixin()

    @patch("source.mixins.Text")
    def test_print_options(self, mock_text, mock_print):
        options = [
            {"name": "option1"},
            {"name": "option2"},
        ]
        self.print_mixin.print_options(options)

        self.assertEqual(mock_text.call_count, 5)
        mock_print.assert_called_once()

    @patch("source.mixins.Padding")
    @patch("source.mixins.Text")
    @patch("source.mixins.Table")
    def test_print_time_info(
        self, mock_table, mock_text, mock_padding, mock_print
    ):
        time_ranges = [
            [datetime(2022, 1, 1, 8, 0), datetime(2022, 1, 1, 9, 0)],
            [datetime(2022, 1, 1, 9, 0), datetime(2022, 1, 1, 10, 0)],
        ]
        self.print_mixin.print_time_info(time_ranges)

        self.assertEqual(mock_table.call_count, 1)
        self.assertTrue(mock_text.called)
        self.assertTrue(mock_padding.called)
        self.assertTrue(mock_print.called)

    @patch("source.mixins.Text")
    @patch("source.mixins.Panel")
    def test_print_suggestion(self, mock_panel, mock_text, mock_print):
        suggestion = "Some suggestion"
        self.print_mixin.print_suggestion(suggestion)

        mock_print.assert_called_once()
        mock_panel.fit.assert_called_once()
        mock_text.assert_called_once()

    @patch("source.mixins.Padding")
    @patch("source.mixins.Text")
    @patch("source.mixins.Table")
    def test_print_booking_info(
        self, mock_table, mock_text, mock_padding, mock_print
    ):
        booking_info = {
            "date": "2022-01-01",
            "start_time": "08:00",
            "end_time": "09:00",
        }
        self.print_mixin.print_booking_info(booking_info)

        self.assertEqual(mock_table.call_count, 1)
        self.assertTrue(mock_text.called)
        self.assertTrue(mock_padding.called)
        self.assertTrue(mock_print.called)

    @patch("source.mixins.Padding")
    @patch("source.mixins.Text")
    def test_print_user_bookings(self, mock_text, mock_padding, mock_print):
        bookings = [
            {
                "booking": {
                    "service": "service1",
                    "date": "2022-01-01",
                    "start_time": "08:00",
                }
            },
            {
                "booking": {
                    "service": "service2",
                    "date": "2022-01-02",
                    "start_time": "09:00",
                }
            },
        ]
        self.print_mixin.print_user_bookings(bookings)

        self.assertTrue(mock_text.called)
        self.assertTrue(mock_padding.called)
        mock_print.assert_called_once()

    @patch("source.mixins.Padding")
    @patch("source.mixins.Text")
    @patch("source.mixins.Panel")
    def test_print_service_info(
        self, mock_panel, mock_text, mock_padding, mock_print
    ):
        service_info = {
            "name": "service1",
            "duration": 1,
            "price": 100,
            "description": "Some description",
        }
        self.print_mixin.print_service_info(service_info)

        self.assertTrue(mock_panel.called)
        self.assertTrue(mock_text.called)
        self.assertTrue(mock_padding.called)
        self.assertTrue(mock_print.called)
