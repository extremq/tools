import os
from termcolor import cprint


def check_for_env_variables(required_env: set[str], group: str):
    present_env = {env for env in os.environ if os.environ[env]}

    if required_env.issubset(present_env):
        return

    missing_env = required_env.difference(present_env)
    raise Exception(
        f"From group {group!r}, "
        f"missing environment variables: {list(missing_env)!r}"
    )


def raise_if_file_not_found(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path!r}")


def print_error(message: str) -> None:
    cprint(f"Error: {message}", color="red", attrs=["bold"])


def print_info(message: str) -> None:
    cprint(f"Info: {message}", color="yellow", attrs=["bold"])


def print_success(message: str) -> None:
    cprint(f"Success: {message}", color="green", attrs=["bold"])
