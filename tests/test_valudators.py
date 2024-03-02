from datetime import date, datetime, time, timedelta
from unittest import TestCase

# Use for mocking date.today https://stackoverflow.com/questions/4481954/trying-to-mock-datetime-date-today-but-not-working
from freezegun import freeze_time

from source.validators import (
    validate_date,
    validate_integer_option,
    validate_name,
    validate_phone_number,
    validate_time,
    validate_yes_no,
)


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


class ValidateYesNo(TestCase):
    def test_valid_yes(self):
        result = validate_yes_no("yes")
        
        self.assertIsNone(result)

    def test_valid_no(self):
        result = validate_yes_no("no")
        
        self.assertIsNone(result)

    def test_invalid_option(self):
        message = "Please enter 'yes' or 'no'."

        with self.assertRaises(ValueError) as context:
            validate_yes_no("invalid-option")
        
        self.assertEqual(str(context.exception), message)


class ValidateTime(TestCase):
    def setUp(self):
        date_obj = date(1999, 12, 31)
        self.time_ranges = [
            [datetime.combine(date_obj, time(8)), datetime.combine(date_obj, time(9))],
            [datetime.combine(date_obj, time(15)), datetime.combine(date_obj, time(16))],
            [datetime.combine(date_obj, time(17)), datetime.combine(date_obj, time(20))],
        ]
    
    def test_valid_time(self):
        data = '08:30'
        result = validate_time(data, self.time_ranges)

        self.assertIsNone(result)
    
    def test_time_not_in_range(self):
        data = '10:00'
        message = "Your time is not in the available time ranges."

        with self.assertRaises(ValueError) as context:
            validate_time(data, self.time_ranges)
        
        self.assertEqual(str(context.exception), message)
    
    def test_invalid_hour(self):
        data = "25:00"
        message = "hour must be in 0..23"
        
        with self.assertRaises(ValueError) as context:
            validate_time(data, self.time_ranges)
        
        self.assertEqual(str(context.exception), message)
    
    def test_invalid_minute(self):
        data = "23:60"
        message = "minute must be in 0..59"
        
        with self.assertRaises(ValueError) as context:
            validate_time(data, self.time_ranges)
        
        self.assertEqual(str(context.exception), message)
    
    def test_invalid_time(self):
        data = "invalid-time"
        message = f"Invalid isoformat string: '{data}'"

        with self.assertRaises(ValueError) as context:
            validate_time(data, self.time_ranges)
        
        self.assertEqual(str(context.exception), message)


class ValidateName(TestCase):
    def test_valid_name(self):
        result = validate_name("John")
        
        self.assertIsNone(result)
    
    def test_name_too_short(self):
        name = "Jo"
        message = "The name must contain 3 to 30 characters."

        with self.assertRaises(ValueError) as context:
            validate_name(name)
        
        self.assertEqual(str(context.exception), message)
    
    def test_name_too_long(self):
        name = "J" * 31
        message = "The name must contain 3 to 30 characters."
        
        with self.assertRaises(ValueError) as context:
            validate_name(name)
        
        self.assertEqual(str(context.exception), message)
    
    def test_name_not_alpha(self):
        data = ["John1", "Jon Doe", "Jon@32", "Jon-"]
        message = "The name must contain only letters."
        
        for name in data:
            with self.assertRaises(ValueError) as context:
                validate_name(name)
        
            self.assertEqual(str(context.exception), message)


class ValidatePhoneNumber(TestCase):
    def test_valid_phone_number(self):
        data = "+353 111111111"
        result = validate_phone_number(data)
        
        self.assertIsNone(result)
    
    def test_long_number(self):
        data = "+420 1111111111"
        massage = f"The number {data} is not valid"
        
        with self.assertRaises(ValueError) as context:
            validate_phone_number(data)

        self.assertEqual(str(context.exception), massage)
    
    def test_short_number(self):
        data = "+420 11111111"
        massage = f"The number {data} is not valid"

        with self.assertRaises(ValueError) as context:
            validate_phone_number(data)
        
        self.assertEqual(str(context.exception), massage)
    
    def test_invalid_country_code(self):
        data = "420 111111111"
        massage = "(0) Missing or invalid default region."

        with self.assertRaises(ValueError) as context:
            validate_phone_number(data)
        
        self.assertEqual(str(context.exception), massage)
    
    def test_invalid_characters(self):
        data = "+420 1111111a1"
        massage = f"The number {data} is not valid"

        with self.assertRaises(ValueError) as context:
            validate_phone_number(data)
        
        self.assertEqual(str(context.exception), massage)
