from datetime import date, timedelta
from unittest import TestCase
from unittest.mock import patch

# Use for mocking date.today https://stackoverflow.com/questions/4481954/trying-to-mock-datetime-date-today-but-not-working
from freezegun import freeze_time

from source.validators import validate_date, validate_integer_option


class ValidateIntegerOption(TestCase):
    def test_valid_integer(self):
        result = validate_integer_option("1", 1, 3)
        
        self.assertIsNone(result)

    def test_integer_less_then_min_numb(self):
        min_numb = 1
        max_numb = 3
        message = f"Please enter a number between {min_numb} and {max_numb} inclusive."

        with self.assertRaises(ValueError) as context:
            validate_integer_option("0", min_numb, max_numb)
        
        self.assertEqual(str(context.exception), message)
    
    def test_integer_greater_then_max_numb(self):
        min_numb = 1
        max_numb = 3
        message = f"Please enter a number between {min_numb} and {max_numb} inclusive."

        with self.assertRaises(ValueError) as context:
            validate_integer_option("4", min_numb, max_numb)
        
        self.assertEqual(str(context.exception), message)
    
    def test_not_integer(self):
        min_numb = 1
        max_numb = 3
        value = "a"
        message = f"invalid literal for int() with base 10: '{value}'"

        with self.assertRaises(ValueError) as context:
            validate_integer_option(value, min_numb, max_numb)
        
        self.assertEqual(str(context.exception), message)


@freeze_time("1999-12-31")
class ValidateDate(TestCase):
    
    def test_valid_date(self):
        data = "1999-12-31"
        result = validate_date(data)

        self.assertIsNone(result)

    def test_date_in_past(self):
        data = "1999-12-30"
        message = f"Your date {data} is in the past. Please enter a future date."

        with self.assertRaises(ValueError) as context:
            validate_date(data)
        
        self.assertEqual(str(context.exception), message)

    def test_invalid_year(self):
        data = "19999-12-31"
        message = f"Invalid isoformat string: '{data}'"

        with self.assertRaises(ValueError) as context:
            validate_date(data)
        
        self.assertEqual(str(context.exception), message)
    
    def test_invalid_month(self):
        data = "1999-13-31"
        message = "month must be in 1..12"

        with self.assertRaises(ValueError) as context:
            validate_date(data)
        
        self.assertEqual(str(context.exception), message)
    
    def test_invalid_day(self):
        data = "1999-12-32"
        message = "day is out of range for month"

        with self.assertRaises(ValueError) as context:
            validate_date(data)
        
        self.assertEqual(str(context.exception), message)
    
    def test_invalid_date(self):
        data = "invalid-date"
        message = f"Invalid isoformat string: '{data}'"

        with self.assertRaises(ValueError) as context:
            validate_date(data)
        
        self.assertEqual(str(context.exception), message)
