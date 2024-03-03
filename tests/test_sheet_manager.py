from unittest import TestCase
from unittest.mock import MagicMock

from source.sheet_manager import SpaSheet
from datetime import datetime, time, date, timedelta

SPA_INFO = [
            {"name": "service1", "type": "main", "description": "description1", "price": "10", "duration": 2},
            {"name": "service2", "type": "sub", "description": "description2", "price": "20", "duration": 2},
            {"name": "service3", "type": "main", "description": "description3", "price": "30", "duration": 3},
            {"name": "service4", "type": "sub", "description": "description4", "price": "40", "duration": 4},
        ]
BOOKING_DATA = [
            {
                "service": "service1",
                "name": "Den",
                "phone_number": 353111111111,
                "start_time": "08:00",
                "end_time": "10:00",
                "date": "2024-02-26",
                "additional_service": "additional_service1",
            },
            {
                "service": "service1",
                "name": "John",
                "phone_number": 353222222222,
                "start_time": "10:00",
                "end_time": "12:00",
                "date": "2024-02-26",
                "additional_service": "additional_service2",
            },
            {
                "service": "service3",
                "name": "Jane",
                "phone_number": 353333333333,
                "start_time": "12:00",
                "end_time": "15:00",
                "date": "2024-02-26",
                "additional_service": "additional_service3",
            },
            {
                "service": "service4",
                "name": "Den",
                "phone_number": 353111111111,
                "start_time": "15:00",
                "end_time": "19:00",
                "date": "2024-02-26",
                "additional_service": "additional_service4",
            },
            {
                "service": "service1",
                "name": "John",
                "phone_number": 353222222222,
                "start_time": "19:00",
                "end_time": "21:00",
                "date": "2024-02-26",
                "additional_service": "additional_service1",
            },
]
WORKSHEET_NAMES_DATA = {"spa_info": SPA_INFO, "booking_data": BOOKING_DATA}


class MockSpreadsheet(MagicMock):
    def worksheets(self):
        result = []
        for name, data in WORKSHEET_NAMES_DATA.items():
            worksheet = MagicMock()
            worksheet.title = name
            worksheet.get_all_records.return_value = data
            result.append(worksheet)
        return result


class TestSpaSheet(TestCase):
    def setUp(self):
        self.worksheet_names = WORKSHEET_NAMES_DATA.keys()
        self.mock_spreadsheet = MockSpreadsheet()
        self.sheet = SpaSheet(self.mock_spreadsheet)
        self.services = SPA_INFO
        self.bookings = BOOKING_DATA

    def test_init_(self):
        for worksheet_name in self.worksheet_names:
            self.assertTrue(hasattr(self.sheet, worksheet_name))
    
    def test_get_all_services(self):
        result = self.sheet.get_services()
        self.assertEqual(result, self.services)

    def test_get_main_services(self):
        _type = "main"
        result = self.sheet.get_services(_type)
        
        self.assertTrue(all(service["type"] == _type for service in result))
    
    def test_get_sub_services(self):
        _type = "sub"
        result = self.sheet.get_services(_type)
        
        self.assertTrue(all(service["type"] == _type for service in result))
    
    def test_invalid_service_type(self):
        _type = "invalid"
        result = self.sheet.get_services(_type)
        
        self.assertEqual(result, [])
    
    def test_get_service_info(self):
        service = "service1"
        field_name = "description"
        result = self.sheet.get_service_info(service, field_name)

        self.assertEqual(result, "description1")

    def test_service_not_found(self):
        service = "invalid_service"
        field_name = "description"
        message = "Service not found"
        result = self.sheet.get_service_info(service, field_name)

        self.assertEqual(result, message)

    def test_get_available_times_for_date_and_service(self):
        date_str = "2024-02-26"
        service = "service1"
        expected_result = [[datetime(2024, 2, 26, 12, 0), datetime(2024, 2, 26, 14, 0)],
                           [datetime(2024, 2, 26, 13, 0), datetime(2024, 2, 26, 15, 0)],
                           [datetime(2024, 2, 26, 14, 0), datetime(2024, 2, 26, 16, 0)],
                           [datetime(2024, 2, 26, 15, 0), datetime(2024, 2, 26, 17, 0)],
                           [datetime(2024, 2, 26, 16, 0), datetime(2024, 2, 26, 18, 0)],
                           [datetime(2024, 2, 26, 17, 0), datetime(2024, 2, 26, 19, 0)]
                           ]
        result = self.sheet.get_available_times_for_date_and_service(date_str, service)

        self.assertEqual(result, expected_result)
    
    def test_no_available_times(self):
        # Fill up the day with bookings
        service_data = self.services[0]
        date_str = "2024-12-31"
        date_obj = date.fromisoformat(date_str)
        service_duration = timedelta(hours=service_data["duration"])
        first_start_time = datetime.combine(date_obj, time.fromisoformat("08:00"))
        last_end_time = datetime.combine(date_obj, time.fromisoformat("21:00"))
        while True:
            end_time = first_start_time + service_duration
            if end_time > last_end_time:
                break
            booking = {
                "service": service_data["name"],
                "start_time": first_start_time.time().isoformat(),
                "end_time": (end_time).time().isoformat(),
                "date": date_str,
            }
            self.bookings.append(booking)
            first_start_time = end_time
        
        result = self.sheet.get_available_times_for_date_and_service(date_str, service_data["name"])
        self.assertEqual(result, [])
    
    def test_all_day_free(self):
        date_str = "2024-12-31"
        service = self.services[0]
        service_name = service["name"]
        duration = service["duration"]
        available_amount_bookings_for_service = 0
        open_time = 8 # 08:00
        close_time = 21  # 21:00

        # Calculate the amount of available bookings in one day for the service
        while True:
            if open_time + duration > close_time:
                break
            available_amount_bookings_for_service += 1
            open_time += 1
        result = self.sheet.get_available_times_for_date_and_service(date_str, service_name)

        self.assertEqual(len(result), available_amount_bookings_for_service)
