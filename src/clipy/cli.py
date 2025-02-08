import argparse
import functools
from typing import Any, Callable, List

from .cli_types import CommandDefinition, OptionDefinition


class CLI:
    """
    Wrapper class for a CLI application.

    Attributes:
    :param func: Main function of the CLI application.
    :param usage: Usage string for the CLI application.
    :param description: Description string for the CLI application.
    :param commands: List of `CommandDefinition` instances for the CLI application. Default is an empty list.
    :param global_options: List of `OptionDefinition` instances for the CLI application. Default is an empty list.

    Methods:
    :method register_command: Register a command to the CLI application.
    :method register_global_option: Register a global option to the CLI application.
    :method build_parser: Build an `argparse.ArgumentParser` instance for the CLI application.
    """

    commands: List[CommandDefinition]
    global_options: List[OptionDefinition]
    func: Callable[..., Any]

    def __init__(self, func: Callable[..., Any], usage: str = None, description: str = None):
        self.func = func

        self.usage = usage
        self.description = description

        self.commands = []
        self.global_options = []
        functools.update_wrapper(self, func)

    def register_command(self, command: CommandDefinition):
        self.commands.append(command)

    def register_global_option(self, option: OptionDefinition):
        self.global_options.append(option)

    def build_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(usage=self.usage, description=self.description)

        for option in self.global_options:
            parser.add_argument(f"--{option.name}", **option.kwargs)

        subparsers = parser.add_subparsers(dest="command")

        for command in self.commands:
            subp = subparsers.add_parser(
                command.name, usage=command.usage, description=command.description
            )
            for option in command.options:
                subp.add_argument(f"--{option.name}", **option.kwargs)

        return parser

    def __call__(self, *args, **kwargs):
        parser = self.build_parser()

        parsed_args = parser.parse_args()
        args_dict = vars(parsed_args)

        command_name = args_dict.pop("command")
        command = CommandDefinition(name=command_name, options=args_dict)

        return self.func(command=command, *args, **kwargs)
