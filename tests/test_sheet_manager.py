from unittest import TestCase
from unittest.mock import MagicMock

from source.sheet_manager import SpaSheet

SPA_INFO = [
            {"name": "service1", "type": "main", "description": "description1", "price": "10", "duration": "1"},
            {"name": "service2", "type": "sub", "description": "description2", "price": "20", "duration": "2"},
            {"name": "service3", "type": "main", "description": "description3", "price": "30", "duration": "3"},
            {"name": "service4", "type": "sub", "description": "description4", "price": "40", "duration": "4"},
        ]
BOOKING_DATA = []
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
    