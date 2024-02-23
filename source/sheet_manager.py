from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import Literal

from gspread import Spreadsheet


class SpaSheet:
    """Class to manage sheet data"""

    def __init__(self, sheet: Spreadsheet):
        self.sheet = sheet

        # Loop through all the worksheets and set them as properties
        for work_sheet in self.sheet.worksheets():
            setattr(self, work_sheet.title, work_sheet)

    def get_services(self, service_type: Literal[None, "main", "sub"] = None) -> list[dict]:
        """Get services from the sheet based on the service_type provided.
        If the service_type is None, it will return all services.
        If the service_type is 'main' or 'sub' it will return services with respective type.

        Args:
            service_type (Literal[None, "main", "sub"], optional): type of service. Defaults to None.

        Returns:
            list[dict]: List of services
        """

        if service_type:
            result = [
                service
                for service in self.spa_info.get_all_records()
                if service["type"] == service_type
            ]
        else:
            result = self.spa_info.get_all_records()

        return result

    def get_service_info(self, service: str, field_name: str) -> str:
        """Get the information for a particular service field

        Args:
            service (str): Service name
            field_name (str): Service field to get information from

        Returns:
            str: The service information which is contained in the field_name
        """
        services = self.spa_info.get_all_records()

        for service_data in services:
            if service_data["name"] == service:
                return service_data[field_name]
        
        return "Service not found"

    def get_available_times_for_date_and_service(self, date_str: str, service: str) -> list[list[datetime]]:
        """Calculates available ranges for booking and returns them.

        Args:
            date_str (str): The date to check for available time
            service (str): The service to check for available time

        Returns:
            list[list[datetime]: List of available time
        """
        # Define the open and close time for the spa
        open_time = time.fromisoformat("08:00")
        close_time = time.fromisoformat("21:00")

        # Convert the date string to date object
        date_obj = date.fromisoformat(date_str)

        # Get all bookings and the duration of the service
        all_bookings = self.booking_data.get_all_records()

        # Define timedelta object for duration of selected service
        service_duration = timedelta(hours=self.get_service_info(service, "duration"))

        service_date_bookings = []

        # Loop through all bookings and get the bookings for the service and date
        for booking in all_bookings:
            booking_date_obj = date.fromisoformat(booking["date"])
            if booking["spa_name"] == service and booking_date_obj == date_obj:
                service_date_bookings.append(booking)
        
        # Sort the bookings by start time
        service_date_bookings.sort(key=lambda x: time().fromisoformat(x["start_time"]))

        available_times = []
        for index in range(len(service_date_bookings) + 1):
            if index == 0:
                start_time = open_time
            else:
                start_time = time.fromisoformat(service_date_bookings[index - 1]["end_time"])
            
            if index == len(service_date_bookings):
                end_time = close_time
            else:
                end_time = time.fromisoformat(service_date_bookings[index]["start_time"])
            
            # Convert to datetime object to add the service duration
            start_time = datetime.combine(date_obj, start_time)
            end_time = datetime.combine(date_obj, end_time)

            # Create a ranges of available booking times
            while service_duration + start_time <= end_time:
                available_times.append([start_time, start_time + service_duration])
                start_time += timedelta(hours=1)
            
        return available_times
