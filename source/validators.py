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
