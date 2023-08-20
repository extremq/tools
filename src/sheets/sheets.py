import os
import argparse
from src.tool import Tool
from src.utils import print_error, print_success, print_info
from src.sheets.df import *


class Sheets(Tool):
    @property
    def required_env_variables(self) -> set[str]:
        return {"GOOGLE_SHEETS_CONFIG_FILE"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.spreadsheet_id = None
        self.sheet_name = None
        self.data_file = None
        self.unique_column = None
        self.credentials_path = os.getenv("GOOGLE_SHEETS_CONFIG_FILE")

        if not os.path.exists(self.credentials_path):
            raise ValueError(f"The config file {os.getenv('GOOGLE_SHEETS_CONFIG_FILE')} does not exist")

    def add_argument_group(self, subparsers) -> None:
        sheets = subparsers.add_parser(self.group)
        sheets.add_argument(
            "--data-file", "-d",
            help="The path to the data file which contains the data you want to add to the spreadsheet",
            type=str,
            required=True,
            dest="data_file"
        )

        sheets.add_argument(
            "--spreadsheet-id", "-s",
            help="The id of the spreadsheet you want to add the data to",
            type=str,
            required=True,
            dest="spreadsheet_id"
        )

        sheets.add_argument(
            "--sheet-name", "-n",
            help="The name of the sheet you want to add the data to, if not specified, the first sheet will be used",
            type=str,
            dest="sheet_name"
        )

        sheets.add_argument(
            "--unique-column", "-u",
            help="The column which contains unique values, if not specified, the first column will be used",
            type=str,
            dest="unique_column"
        )

    def check_arguments(self, arguments: argparse.Namespace) -> None:
        if not os.path.exists(arguments.data_file):
            raise ValueError(f"The data file {arguments.data_file!r} does not exist")

        # Get the extension of the data file
        _, extension = os.path.splitext(arguments.data_file)
        SUPPORTED_EXTENSIONS = (".csv",)
        if extension not in SUPPORTED_EXTENSIONS:
            raise ValueError(f"The data file {arguments.data_file!r} is a {extension!r} file."
                             f" I only support {SUPPORTED_EXTENSIONS!r}")

        self.spreadsheet_id = arguments.spreadsheet_id
        self.credentials_path = os.getenv("GOOGLE_SHEETS_CONFIG_FILE")
        self.data_file = arguments.data_file
        self.sheet_name = arguments.sheet_name
        self.unique_column = arguments.unique_column

    def run(self, arguments: argparse.Namespace) -> None:
        df = convert_to_dataframe(self.data_file)
        print_info(f"Successfully converted {self.data_file!r} to a dataframe")

        append_to_google_sheets(df, self.spreadsheet_id, self.credentials_path, self.sheet_name, self.unique_column)
