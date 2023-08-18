import argparse
from .utils import check_for_env_variables
from abc import ABC, abstractmethod


class Tool(ABC):
    @property
    def required_env_variables(self) -> set[str]:
        return set()

    def __init__(self, group: str):
        self.group = group

        check_for_env_variables(self.required_env_variables, self.group)

    @abstractmethod
    def add_argument_group(self, subparsers) -> None:
        raise NotImplementedError

    @abstractmethod
    def check_arguments(self, arguments: argparse.Namespace) -> None:
        raise NotImplementedError

    @abstractmethod
    def run(self, arguments: argparse.Namespace) -> None:
        raise NotImplementedError
