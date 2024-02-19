from source.mixins import PrintMixin
from source.sheet_manager import SpaSheet
from source.validators import validate_integer_option


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

    def __init__(self, sheet: SpaSheet):
        self.sheet = sheet
        self.run_flow()

    def run_flow(self):
        pass


class BookingFlow(BasicFlow):
    """Class to manage booking"""

    def run_flow(self):
        self.choose_service()

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
        print(input_value)


class CancelFlow(BasicFlow):
    """Class to manage cancellation"""

    def run_flow(self):
        print("Cancel flow")


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

        self.FLOW_OPTIONS[int(option)]["object"](self.sheet)
