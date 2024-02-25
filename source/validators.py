from __future__ import annotations

from datetime import date, datetime, time

import phonenumbers


def validate_integer_option(option: str, min_numb: int = 0, max_numb: int = 3) -> None:
    """Check if the option is a number between min_numb and max_numb inclusive

    Args:
        option (str): The option to check
        min_numb (int, optional): The minimum number allowed. Defaults to 0.
        max_numb (int, optional): The maximum number allowed. Defaults to 3.

    Raises:
        ValueError: If the option is not a number between min_numb and max_numb inclusive
    """

    option = int(option)

    if not (min_numb <= option <= max_numb):
        message = f"Please enter a number between {min_numb} and {max_numb} inclusive."
        raise ValueError(message)


def validate_date(option: str):
    """Check if the option is a date in format YYYY-MM-DD and if the date is not in the past

    Args:
        option (str): date string for validation
    """

    date_obj = date.fromisoformat(option)

    if date_obj < date.today():
        message = f"Your date {date_obj.isoformat()} is in the past. Please enter a future date."
        raise ValueError(message)


def validate_yes_no(option: str):
    """Check if the option is a 'yes' or 'no' string

    Args:
        option (str): The option to check

    Raises:
        ValueError: If the option is not 'yes' or 'no'
    """

    if option.lower() not in ["yes", "no"]:
        message = "Please enter 'yes' or 'no'."
        raise ValueError(message)


def validate_time(option: str, time_ranges: list[list[datetime]]) -> None:
    """Check if the option is a time in format HH:MM and  in time_ranges list

    Args:
        option (str): The option to check
        time_ranges (list[list[datetime]]): List of available times

    Raises:
        ValueError: If the option is not a number between 0 and the length of time_ranges list
    """

    time_obj = time.fromisoformat(option)

    for time_range in time_ranges:
        if time_range[0].time() <= time_obj <= time_range[-1].time():
            break
    else:
        message = "Your time is not in the available time ranges."
        raise ValueError(message)


def validate_name(name: str) -> None:
    """Check if the name is a string with length 3 to 30 characters
    and if it contains only letters.

    Args:
        name (str): The word to check
    """
    
    if not (3 <= len(name) <= 30):
        message = "The name must contain 3 to 30 characters."
        raise ValueError(message)

    if not name.isalpha():
        message = "The name must contain only letters."
        raise ValueError(message)


def validate_phone_number(phone_number: str) -> None:
    """Check if the phone number is valid. The number must be in the format +CCC NNNNNNNNNN
    where C is the country code and N is the number.

    Args:
        phone_number (str): The phone number to check
    
    Raises:
        ValueError: If the phone number is not valid
    """
    try:
        phone_obj = phonenumbers.parse(phone_number, None)
    except phonenumbers.phonenumberutil.NumberParseException as ex:
        message = str(ex)
        raise ValueError(message) from ex

    if not phonenumbers.is_valid_number(phone_obj):
        message = f"The number {phone_number} is not valid"
        raise ValueError(message)
