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
