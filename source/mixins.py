from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


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

    def print_time_info(self, time_ranges: list[list[datetime]]) -> None:
        """Prints the booking times.

        Args:
            times (list[list[datetime]]): List of available times
        """

        for time_range in time_ranges:
            print(f"{time_range[0].strftime('%H:%M')} - {time_range[-1].strftime('%H:%M')}")
