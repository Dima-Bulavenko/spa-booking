from __future__ import annotations

from typing import TYPE_CHECKING

from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

if TYPE_CHECKING:
    from datetime import datetime


print_theme = Theme({
    "options": "green",
    "error": "red",
    "info": "blue bold",
    "input": "purple",
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

        console.print(Padding(message, (0, 2, 0, 2)))

    def print_time_info(self, time_ranges: list[list[datetime]]) -> None:
        """Prints the booking times.

        Args:
            times (list[list[datetime]]): List of available times
        """

        table = Table("Start time", "End time", title=Text("Available times", style="info"))
        for time_range in time_ranges:
            start_time = Text(time_range[0].strftime("%H:%M"), style="options")
            end_time = Text(time_range[-1].strftime("%H:%M"), style="options")
            table.add_row(start_time, end_time, end_section=True)
        console.print(Padding(table, (1, 0)))

    def print_suggestion(self, suggestion: str) -> None:
        """Prints the suggestion message.

        Args:
            suggestion (str): The suggestion message
        """
        message = Panel.fit(Text(suggestion, style="info"))
        console.print(message)
    
    def print_booking_info(self, booking_info: dict) -> None:
        """Prints the booking information.

        Args:
            booking_info (dict): The booking information
        """
        table = Table(title=Text("Booking information", style="info"), show_header=False)
        for key, value in booking_info.items():
            name = Text(f"{key}: ", style="info")
            data = Text(value, style="options")
            table.add_row(name, data, end_section=True)
        console.print(Padding(table, (1, 0)))
    
    def print_user_bookings(self, bookings: list[dict]) -> None:
        """Prints the user bookings.

        Args:
            user_bookings (list[dict]): List of user bookings
        """
        messages = []
        for index, booking_data in enumerate(bookings):
            booking = booking_data["booking"]
            message = Text(f"{index}. {booking['service']} on {booking['date']} at {booking['start_time']}",
                           style="options")
            messages.append(message)
        messages = Padding(Text("\n").join(messages), (0, 2, 0, 2))
        console.print(messages)
