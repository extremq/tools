import argparse
from src.tool import Tool
from src.utils import print_error, print_success, print_info
from src.lol.api import *


class LeagueOfLegends(Tool):
    @property
    def required_env_variables(self) -> set[str]:
        return {"LEAGUE_API_KEY"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.summoner_name = None
        self.puuid = None
        self.region = None

        self.match_history = []
        self.match_data = []

        self.today = datetime.date.today().strftime("%Y-%m-%d")
        self.start_date = None
        self.end_date = None

    def add_argument_group(self, subparsers) -> None:
        lol = subparsers.add_parser(self.group)
        lol.add_argument(
            "--start-date", "-s",
            help="From which date you want to get the matches (Example: 2027-01-01)",
            type=str,
            dest="start_date",
            default=self.today
        )

        lol.add_argument(
            "--end-date", "-e",
            help="To which date you want to get the matches (Example: 2027-01-01)",
            type=str,
            dest="end_date",
            default=self.today
        )

        lol.add_argument(
            "--summoner-name", "-n",
            help="The summoner name you want to get the matches from",
            type=str,
            dest="summoner_name",
            required=True
        )

        lol.add_argument(
            "--region", "-r",
            help="The region of the summoner name you want to get the matches from (Example: EUW1, euw1, EUN1, eun1)",
            type=str,
            dest="region",
            required=True
        )

        lol.add_argument(
            "--output", "-o",
            help="The output file",
            type=str,
            dest="output",
            default="output.csv"
        )

    def check_arguments(self, arguments: argparse.Namespace) -> None:
        if arguments.start_date > arguments.end_date:
            raise ValueError("Start date must be before or equal to end date")

        if arguments.start_date > self.today:
            print_info("Start date is in the future, setting it to today")
            arguments.start_date = self.today

        self.summoner_name = arguments.summoner_name
        self.start_date = arguments.start_date
        self.end_date = arguments.end_date
        self.region = arguments.region

    def run(self, arguments: argparse.Namespace) -> None:
        self.puuid = get_puuid(self.summoner_name, self.region)
        print_info(f"Found summoner {self.summoner_name!r} with puuid {self.puuid!r}.")

        self.match_history = get_match_history(self.puuid, self.start_date, self.end_date)
        print_info(f"Finished getting {len(self.match_history)!r} matches.")

        self.match_data = turn_data_to_dataframe(self.match_history, self.puuid)
        print_info(f"Turned data into dataframe.")
        print_info(f"First 5 rows of dataframe:\n{self.match_data.head(5)}")

        if arguments.output.endswith(".csv"):
            self.match_data.to_csv(arguments.output, index=False, encoding="utf-8")
        elif arguments.output.endswith(".xlsx"):
            self.match_data.to_excel(arguments.output, index=False)

        print_success(f"Successfully saved {len(self.match_data)!r} matches to {arguments.output!r}.")
