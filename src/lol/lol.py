import argparse

from src.tool import Tool


class LeagueOfLegends(Tool):
    @property
    def required_env_variables(self) -> set[str]:
        return {"LEAGUE_OF_LEGENDS_API_KEY"}

    def add_argument_group(self, subparsers) -> None:
        pass

    def check_arguments(self, arguments: argparse.Namespace) -> None:
        pass

    def run(self, arguments: argparse.Namespace) -> None:
        pass
