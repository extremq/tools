import os
import argparse
from src.tool import Tool
import requests


def _get_exchange_rates():
    url = f'https://openexchangerates.org/api/latest.json?app_id={os.getenv("OPEN_EXCHANGE_RATES_APP_ID")}'
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Cannot get exchange rates.")

    return response.json()


class MoneyLost(Tool):
    @property
    def required_env_variables(self) -> set[str]:
        return {"OPEN_EXCHANGE_RATES_APP_ID"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.exchange_rates = _get_exchange_rates()
        self.from_currency = {
            "code": None,
            "rate": None
        }

        self.to_currency = {
            "code": None,
            "rate": None
        }

        self.sold_amount = None
        self.bought_amount = None

    def add_argument_group(self, subparsers) -> None:
        money_lost = subparsers.add_parser(self.group)
        money_lost.add_argument(
            "--from", "-f",
            help="From which currency you converted (Example: EUR, eur, ron, USD)",
            type=str,
            required=True,
            dest="from_currency"
        )

        money_lost.add_argument(
            "--to", "-t",
            help="To which currency you converted (Example: EUR, eur, ron, USD)",
            type=str,
            required=True,
            dest="to_currency"
        )

        money_lost.add_argument(
            "--sold", "-s",
            help="Amount of money you sold",
            type=float,
            required=True,
            dest="sold_amount"
        )

        money_lost.add_argument(
            "--bought", "-b",
            help="Amount of money you bought",
            type=float,
            required=True,
            dest="bought_amount"
        )

    def check_arguments(self, arguments: argparse.Namespace) -> None:
        if arguments.from_currency.upper() == arguments.to_currency.upper():
            raise ValueError(f"From currency ({arguments.from_currency.upper()!r}) "
                             f"and To currency ({arguments.to_currency.upper()!r}) cannot be the same.")

        if arguments.sold_amount <= 0:
            raise ValueError(f"Sold amount ({arguments.sold_amount!r}) must be greater than 0.")

        if arguments.bought_amount <= 0:
            raise ValueError(f"Bought amount ({arguments.bought_amount!r}) must be greater than 0.")

        if arguments.from_currency.upper() not in self.exchange_rates["rates"]:
            raise ValueError(f"From currency ({arguments.from_currency.upper()!r}) is not supported.")

        if arguments.to_currency.upper() not in self.exchange_rates["rates"]:
            raise ValueError(f"To currency ({arguments.to_currency.upper()!r}) is not supported.")

        self.from_currency = {
            "code": arguments.from_currency.upper(),
            "rate": self.exchange_rates["rates"][arguments.from_currency.upper()]
        }

        self.to_currency = {
            "code": arguments.to_currency.upper(),
            "rate": self.exchange_rates["rates"][arguments.to_currency.upper()]
        }

        self.sold_amount = arguments.sold_amount
        self.bought_amount = arguments.bought_amount

    def run(self, arguments: argparse.Namespace) -> None:
        user_exchange_rate = self.sold_amount / self.bought_amount
        real_exchange_rate = self.from_currency["rate"] / self.to_currency["rate"]

        print(f" Your rate: {user_exchange_rate:10.3f} {self.from_currency['code']} / per {self.to_currency['code']}")
        print(f" Real rate: {real_exchange_rate:10.3f} {self.from_currency['code']} / per {self.to_currency['code']}")
        print()

        real_bought_amount = self.sold_amount / real_exchange_rate
        difference = real_bought_amount - self.bought_amount

        print(f"Your value: {self.bought_amount:10.3f} {self.to_currency['code']}")
        print(f"Real value: {real_bought_amount:10.3f} {self.to_currency['code']}")
        print("-" * 30)
        print(f"Difference: {difference:10.3f} {self.to_currency['code']}")
