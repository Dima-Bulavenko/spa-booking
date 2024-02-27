from datetime import date, datetime, time, timedelta

from source.mixins import PrintMixin
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
        value = input(prompt + "\n")
        try:
            validator(value, *args, **kwargs)
        except ValueError as e:
            print(f"Invalid input: {e}")
        else:
            break
    return value


class BasicFlow(PrintMixin):
    """Class to manage basic flow"""

    def __init__(self, sheet: SpaSheet, controller: "FlowController"):
        self.sheet = sheet
        self.controller = controller
        self.info = {}

        self.run_flow()

    def run_flow(self):
        print(f"run_flow method not implemented for {self.__class__.__name__}")


class BookingFlow(BasicFlow):
    """Class to manage booking"""

    def run_flow(self):
        self.choose_service()
        self.choose_additional_services()
        self.choose_date_time()
        self.input_credentials()
        self.submit_or_change_booking_data()
        self.save_booking()
        self.show_success_message()

    def choose_service(self):
        services = self.sheet.get_services("main")

        print("Choose a service:")
        self.print_options(services)

        input_value = input_handler(
            "Enter service number:",
            validate_integer_option,
            min_numb=0,
            max_numb=len(services) - 1,
        )

        # Save the chosen service to the info dictionary
        self.info["service"] = services[int(input_value)]["name"]

    def choose_additional_services(self):
        print("Do you want to add any additional services?")

        yes_no = input_handler("Enter 'yes' or 'no':", validate_yes_no)
        if yes_no == "yes":
            additional_services = self.sheet.get_services("sub")
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
        print("Choose the date when you want to visit us.")

        date_visit = input_handler("Enter the date in format YYYY-MM-DD:", validate_date)

        time_ranges = self.sheet.get_available_times_for_date_and_service(date_visit, self.info["service"])

        print("Choose the time when you want to visit us.")
        self.print_time_info(time_ranges)
        
        time_visit = input_handler("Enter the time in format HH:MM:", validate_time, time_ranges=time_ranges)
        
        self.info["date"] = date_visit
        self.info["start_time"] = time_visit

        # Calculate the end time based on the start time and the duration of the service
        duration = float(self.sheet.get_service_info(self.info["service"], "duration"))
        end_time = datetime.combine(date.fromisoformat(date_visit),
                                    time.fromisoformat(time_visit)) + timedelta(hours=duration)
        self.info["end_time"] = end_time.time().isoformat("minutes")

    def input_credentials(self):
        print("Please enter your name")

        name = input_handler("Enter your name:\n(it must contain only letters and 3 to 30 characters)", validate_name)
        phone_number = input_handler("Enter your phone number in format +353 111111111:",
                                     validate_phone_number)
        
        self.info["name"] = name
        self.info["phone_number"] = phone_number
    
    def submit_or_change_booking_data(self):
        change_fields = [
            {"name": "Service", "method": self.choose_service},
            {"name": "Additional services", "method": self.choose_additional_services},
            {"name": "Date and time", "method": self.choose_date_time},
            {"name": "Name and phone number", "method": self.input_credentials},
        ]
        while True:
            print("Your booking information:")
            for key, value in self.info.items():
                print(f"{key}: {value}")
            print("Do you want change your booking data?")
            yes_no = input_handler("Enter 'yes' or 'no':", validate_yes_no)
            if yes_no == "yes":
                self.print_options(change_fields)
                field_index = input_handler("Enter the number of the field you want to change:",
                                            validate_integer_option, min_numb=0, max_numb=len(change_fields) - 1)
                change_fields[int(field_index)]["method"]()
            else:
                break
            
    def save_booking(self):
        booking_data = []

        bookings = self.sheet.booking_data
        for key in bookings.get_all_records()[0]:
            booking_data.append(self.info.get(key, ""))
        
        bookings.append_row(booking_data)
    
    def show_success_message(self):
        print("Your booking has been successfully saved.")
        
        print(f"Service: {self.info['service']}")
        print(f"Date: {self.info['date']}")
        print(f"Time: {self.info['start_time']} - {self.info['end_time']}")
        print(f"Name: {self.info['name']}")
        

class CancelFlow(BasicFlow):
    """Class to manage cancellation"""

    def run_flow(self):
        self.input_credentials()

    def input_credentials(self):
        while True:
            print("Please enter your name and phone number with which you made the booking.")

            name = input_handler("Enter your name:\n(it must contain only letters and 3 to 30 characters)",
                                 validate_name)
            phone_number = input_handler("Enter your phone number in format +353 111111111:",
                                        validate_phone_number)
            
            self.info["name"] = name
            self.info["phone_number"] = phone_number
            user_bookings = self.look_for_booking()
            
            if not user_bookings:
                print(f"No bookings found for the provided name '{name}' and phone number '{phone_number}'.")
                print("Do you want to try again?")
                yes_no = input_handler("Enter 'yes' or 'no':", validate_yes_no)
                if yes_no == "yes":
                    continue
                self.controller.manage_options()
            break
        self.info["user_bookings"] = user_bookings
        
        
class AvailabilityFlow(BasicFlow):
    """Class to manage availability"""

    def run_flow(self):
        print("Availability flow")


class TreatmentInfoFlow(BasicFlow):
    """Class to manage treatment information"""

    def run_flow(self):
        print("Treatment info flow")


class FlowController(PrintMixin):
    """Class to manage flow control"""

    FLOW_OPTIONS = (
        {"name": "Book spa treatment", "object": BookingFlow},
        {"name": "Cancel booking", "object": CancelFlow},
        {"name": "Check availability", "object": AvailabilityFlow},
        {"name": "Treatment information", "object": TreatmentInfoFlow},
    )

    def __init__(self, sheet: SpaSheet):
        self.sheet = sheet
        self.current_flow = None

        print("Welcome to the Spa Booking System")

        self.manage_options()

    def manage_options(self):
        while True:
            print("Please select an option:")
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
