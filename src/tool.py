import argparse
from .utils import check_for_env_variables


class Tool(object):
    required_env_variables = set()

    def __init__(self, group: str):
        self.group = group

        check_for_env_variables(self.required_env_variables, self.group)

    def add_argument_group(self, subparsers):
        raise NotImplementedError

    def check_arguments(self, arguments: argparse.Namespace):
        raise NotImplementedError

    def run(self, arguments: argparse.Namespace):
        raise NotImplementedError
