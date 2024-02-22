from datetime import date


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

