import argparse
from dotenv import load_dotenv
from src.utils import raise_if_file_not_found, print_error, print_success
from src.money_lost import MoneyLost
from src.tool import Tool


def setup_env(config_file_name: str = "config.env") -> None:
    raise_if_file_not_found(config_file_name)
    load_dotenv(config_file_name)

    print_success("Environment variables loaded successfully.")


def parser_setup(tools: list[Tool]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tools for everyday life.")

    subparsers = parser.add_subparsers(dest='group', required=True)

    for tool in tools:
        tool.add_argument_group(subparsers)

    return parser.parse_args()


def validate_arguments_and_run(arguments: argparse.Namespace, tools: list[Tool]) -> None:
    for tool in tools:
        if tool.group == arguments.group:
            tool.check_arguments(arguments)
            tool.run(arguments)
            break


def setup_tools() -> None:
    tools = [MoneyLost(group="money_lost")]

    arguments = parser_setup(tools)
    validate_arguments_and_run(arguments, tools)


if __name__ == "__main__":
    try:
        setup_env()
        setup_tools()
    except Exception as e:
        print_error(str(e))
        exit(0)
