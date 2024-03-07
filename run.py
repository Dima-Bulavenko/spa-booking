import gspread
from google.oauth2.service_account import Credentials

from source.flow_controller import FlowController
from source.mixins import console
from source.sheet_manager import SpaSheet

SCOPE = (
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
)
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("spa_booking")


def main():
    with console.status("Loading Spa...", spinner="earth"):
        sheet = SpaSheet(SHEET)
    FlowController(sheet)


if __name__ == "__main__":
    main()
