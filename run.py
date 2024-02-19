import gspread
from google.oauth2.service_account import Credentials

from source.flow_controler import FlowController
from source.sheet_manager import SpaSheet
from source.validators import validate_integer_option

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
    sheet = SpaSheet(SHEET)
    FlowController(sheet)


main()
