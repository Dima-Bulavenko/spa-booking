from __future__ import annotations

from typing import TYPE_CHECKING

from rich.console import Console
from rich.padding import Padding
from rich.text import Text
from rich.theme import Theme

if TYPE_CHECKING:
    from datetime import datetime


print_theme = Theme({
    "options": "green",
    "error": "red",
    "info": "blue",
})

console = Console(theme=print_theme)


class PrintMixin:
    """Class to implement common print methods"""

    def print_options(self, options: list[dict]) -> None:
        """Prints the options provided in format 'index. option_name'.
        Where index is the index of the option in the list and
        the option_name is the name of the specific option.

        Args:
            options (list[dict]): List of options
        """

        message = Text()
        for index, option in enumerate(options):
            index_text = Text(f"{index}. ", style="info")
            option_text = Text(f"{option['name']}\n", style="options")
            message.append(index_text)
            message.append(option_text)

        console.print(Padding(message, 1))

    def print_time_info(self, time_ranges: list[list[datetime]]) -> None:
        """Prints the booking times.

        Args:
            times (list[list[datetime]]): List of available times
        """

        for time_range in time_ranges:
            print(f"{time_range[0].strftime('%H:%M')} - {time_range[-1].strftime('%H:%M')}")
