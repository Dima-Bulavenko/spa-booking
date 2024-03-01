from unittest import TestCase

from source.validators import validate_integer_option


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