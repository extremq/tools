import argparse
from abc import ABC, abstractmethod


class Tool(ABC):
    @property
    def required_env_variables(self) -> set[str]:
        return set()

    def __init__(self, group: str):
        self.group = group

    @abstractmethod
    def add_argument_group(self, subparsers) -> None:
        raise NotImplementedError

    @abstractmethod
    def check_arguments(self, arguments: argparse.Namespace) -> None:
        raise NotImplementedError

    @abstractmethod
    def run(self, arguments: argparse.Namespace) -> None:
        raise NotImplementedError
