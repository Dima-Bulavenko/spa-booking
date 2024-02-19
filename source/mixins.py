from __future__ import annotations


class PrintMixin:
    """Class to implement common print methods"""

    def print_options(self, options: list[dict]) -> None:
        """Prints the options provided in format 'index. option_name'.
        Where index is the index of the option in the list and
        the option_name is the name of the specific option.

        Args:
            options (list[dict]): List of options
        """

        for index, option in enumerate(options):
            print(f"{index}. {option['name']}")
