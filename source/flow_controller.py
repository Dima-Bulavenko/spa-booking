from datetime import date, datetime, time, timedelta
from time import sleep

import phonenumbers
from rich import print
from rich.align import Align
from rich.padding import Padding
from rich.panel import Panel
from rich.text import Text

from source.mixins import PrintMixin, console
from source.sheet_manager import SpaSheet
from source.validators import (
    validate_date,
    validate_integer_option,
    validate_name,
    validate_phone_number,
    validate_space_separated_integers,
    validate_time,
    validate_yes_no,
)


def input_handler(prompt: str, validator: callable, *args, **kwargs) -> str:
    """Invokes the input function and validates the user input using a passed validator

    Args:
        prompt (str): The prompt to display to the user
        validator (callable): The function to use to validate the input
        *args: The positional arguments to pass to the validator
        **kwargs: The keyword arguments to pass to the validator

    Returns:
        str: The validated user input
    """
    while True:
        value = console.input(f"[bold purple]{prompt}" + "\n")
        try:
            validator(value, *args, **kwargs)
        except ValueError as e:
            message = Padding(Panel.fit(Text(f"Invalid input: {e}", style="error")), (0, 0, 1, 0))
            console.print(message)
        else:
            console.clear()
            break
    return value


def formatted_phone_number(phone_number: str) -> str:
    """Parse and return a phone number string in E.164 format

    Args:
        phone_number_str (str): The phone number string to parse and print
    
    Returns:
        str: The phone number in E.164 format
    """
    phone_number = phonenumbers.parse(phone_number, None)
    formatted_phone_number = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
    return formatted_phone_number


class BasicFlow(PrintMixin):
    """Class to manage basic flow"""

    def __init__(self, sheet: SpaSheet, controller: "FlowController"):
        self.sheet = sheet
        self.controller = controller
        self.info = {}

        self.run_flow()

    def run_flow(self):
        print(f"run_flow method not implemented for {self.__class__.__name__}")
    
    def choose_date(self):
        date_visit = input_handler("Enter the date in format YYYY-MM-DD:", validate_date)
        self.info["date"] = date_visit
    
    def choose_time(self, time_ranges: list[list[datetime]]) -> None:
        """Suggest the user to choose the time for the visit based on the available time ranges.
        To use this method, the date, and service must be already chosen
        """
        time_visit = input_handler("Enter the time in format HH:MM:", validate_time, time_ranges=time_ranges)
        
        self.info["start_time"] = time_visit
        # Calculate the end time based on the start time and the duration of the service
        duration = float(self.sheet.get_service_info(self.info["service"], "duration"))
        end_time = datetime.combine(date.fromisoformat(self.info["date"]),
                                    time.fromisoformat(time_visit)) + timedelta(hours=duration)
        self.info["end_time"] = end_time.time().isoformat("minutes")
    
    def choose_service(self, type_str: str = "main") -> None:
        services = self.sheet.get_services(type_str)

        self.print_suggestion("Choose a service:")
        self.print_options(services)

        input_value = input_handler(
            "Enter service number:",
            validate_integer_option,
            min_numb=0,
            max_numb=len(services) - 1,
        )

        self.info["service"] = services[int(input_value)]["name"]
    
    def show_success_message(self, message: str):
        text = Text(message, justify="center", style="info")
        panel = Panel(text)
        aligned_panel = Align.center(panel)
        console.print(aligned_panel)
        console.print(Align.center(Text("You will be taken to main menu", style="option")))
        sleep(4)
        console.clear()


class BookingFlow(BasicFlow):
    """Class to manage booking"""

    def run_flow(self):
        self.choose_service()
        self.choose_additional_services()
        self.choose_date_time()
        self.input_credentials()
        self.submit_or_change_booking_data()
        self.save_booking()
        self.show_success_message("Your booking has been successfully saved.")

    def choose_additional_services(self):
        self.print_suggestion("Do you want to add any additional services?")

        yes_no = input_handler("Enter 'yes' or 'no':", validate_yes_no)
        if yes_no == "yes":
            additional_services = self.sheet.get_services("sub")
            self.print_suggestion("Choose additional service:")
            self.print_options(additional_services)

            input_value = input_handler(
                "Enter additional service number:",
                validate_integer_option,
                min_numb=0,
                max_numb=len(additional_services) - 1,
            )

            # Save the chosen additional service to the info dictionary
            self.info["additional_service"] = additional_services[int(input_value)]["name"]

    def choose_date_time(self):
        self.print_suggestion("Choose the date when you want to visit us.")

        self.choose_date()

        time_ranges = self.sheet.get_available_times_for_date_and_service(self.info["date"], self.info["service"])

        self.print_suggestion("Choose the time when you want to visit us.")
        self.print_time_info(time_ranges)
        
        self.choose_time(time_ranges)
        
    def input_credentials(self):
        self.print_suggestion("Please enter your name")

        name = input_handler("Enter your name:\n(it must contain only letters and 3 to 30 characters)", validate_name)
        self.print_suggestion("Please enter your phone number.")
        phone_number = input_handler("Enter your phone number in format +353 111111111:",
                                     validate_phone_number)
        
        self.info["name"] = name
        self.info["phone_number"] = formatted_phone_number(phone_number)
    
    def submit_or_change_booking_data(self):
        change_fields = [
            {"name": "Service", "method": self.choose_service},
            {"name": "Additional services", "method": self.choose_additional_services},
            {"name": "Date and time", "method": self.choose_date_time},
            {"name": "Name and phone number", "method": self.input_credentials},
        ]
        while True:
            self.print_suggestion("Your booking information:")
            self.print_booking_info(self.info)
            self.print_suggestion("Do you want change your booking data?")
            yes_no = input_handler("Enter 'yes' or 'no':", validate_yes_no)
            if yes_no == "yes":
                self.print_suggestion("Choose the field you want to change:")
                self.print_options(change_fields)
                field_index = input_handler("Enter the number of the field you want to change:",
                                            validate_integer_option, min_numb=0, max_numb=len(change_fields) - 1)
                change_fields[int(field_index)]["method"]()
            else:
                break
            
    def save_booking(self):
        booking_data = []

        bookings = self.sheet.booking_data
        for key in bookings.row_values(1):
            booking_data.append(self.info.get(key, ""))
        
        bookings.append_row(booking_data)
        

class CancelFlow(BasicFlow):
    """Class to manage cancellation"""

    def run_flow(self):
        self.input_credentials()
        self.cancel_booking()
        self.show_success_message("Your bookings has been successfully canceled.")

    def input_credentials(self):
        while True:
            self.print_suggestion("Please enter your name with which you made the booking.")

            name = input_handler("Enter your name:\n(it must contain only letters and 3 to 30 characters)",
                                 validate_name)
            
            self.print_suggestion("Please enter your phone number with which you made the booking.")
            phone_number = input_handler("Enter your phone number in format +353 111111111:",
                                        validate_phone_number)
            
            self.info["name"] = name
            self.info["phone_number"] = phone_number
            user_bookings = self.look_for_booking()
            
            if not user_bookings:
                self.print_suggestion(f"No bookings found for the provided name '{name}' and phone number '{phone_number}'.")
                self.print_suggestion("Do you want to try again?")
                yes_no = input_handler("Enter 'yes' or 'no':", validate_yes_no)
                if yes_no == "yes":
                    continue
                self.controller.manage_options()
            break
        self.info["user_bookings"] = user_bookings
    
    def look_for_booking(self):
        all_bookings = self.sheet.booking_data.get_all_records()
        user_bookings = []
        user_phone = int(self.info["phone_number"].strip("+").replace(" ", ""))
        for row_numb, booking in enumerate(all_bookings):
            if booking["name"] == self.info["name"] and booking["phone_number"] == user_phone:
                user_bookings.append({"booking": booking, "row_number": row_numb + 2})
        return user_bookings

    def cancel_booking(self):
        self.print_suggestion("Your bookings:")
        user_bookings = self.info["user_bookings"]
        self.print_user_bookings(user_bookings)
        
        booking_indexes_str = input_handler("Enter the numbers of the bookings you want to cancel separated by a space:",
                                        validate_space_separated_integers, max_numb=len(user_bookings) - 1)
        booking_indexes = [int(index) for index in booking_indexes_str.split()]
        
        for index_offset, index in enumerate(booking_indexes):
            self.sheet.booking_data.delete_rows(user_bookings[index]["row_number"] - index_offset)
        
        
class AvailabilityFlow(BasicFlow):
    """Class to manage availability"""

    def run_flow(self):
        self.choose_service()
        self.choose_date()
        self.show_result()

    def choose_date(self):
        self.print_suggestion("Enter the date when you want to visit us.")
        super().choose_date()
    
    def show_result(self):
        while True:
            time_ranges = self.sheet.get_available_times_for_date_and_service(self.info["date"], self.info["service"])
            self.print_suggestion(f"Available times for {self.info['service']} on {self.info['date']}:")
            self.print_time_info(time_ranges)
            self.print_suggestion("Do you want to check availability for another date?")
            yes_no = input_handler("Enter 'yes' or 'no':", validate_yes_no)
            if yes_no == "yes":
                self.choose_date()
                continue
            break


class ServiceInfoFlow(BasicFlow):
    """Class to manage service information"""

    def run_flow(self):
        self.choose_service(type_str=None)
        self.show_result()
        
    def show_result(self):
        for service in self.sheet.spa_info.get_all_records():
            if service["name"] == self.info["service"]:
                self.print_service_info(service)
                break
        self.print_suggestion("Do you want to check information for another service?")
        yes_no = input_handler("Enter 'yes' or 'no':", validate_yes_no)
        if yes_no == "yes":
            self.run_flow()


class FlowController(PrintMixin):
    """Class to manage flow control"""

    FLOW_OPTIONS = (
        {"name": "Book spa service", "object": BookingFlow},
        {"name": "Cancel booking", "object": CancelFlow},
        {"name": "Check availability", "object": AvailabilityFlow},
        {"name": "Service information", "object": ServiceInfoFlow},
    )

    def __init__(self, sheet: SpaSheet):
        self.sheet = sheet
        self.current_flow = None

        self.print_suggestion("Welcome to the Spa Booking System")

        self.manage_options()

    def manage_options(self):
        while True:
            self.print_suggestion("Please select an option")
            self.print_options(self.FLOW_OPTIONS)
            
            input_value = input_handler(
                "Enter option number:",
                validate_integer_option,
                min_numb=0,
                max_numb=len(self.FLOW_OPTIONS) - 1,
            )
            self.create_flow(input_value)

    def create_flow(self, option: str):
        """Creates a flow object based on the selected option

        Args:
            option (str): index of a flow in the FLOW_OPTIONS list
        """

        self.FLOW_OPTIONS[int(option)]["object"](self.sheet, self)
