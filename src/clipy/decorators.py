import abc
from typing import Any, Callable, List

from .cli import CLI
from .cli_types import CommandDefinition, OptionDefinition


class CLIDecorator(abc.ABC):
    @staticmethod
    def ensure_cli_wrapper(func: Callable[..., Any]) -> CLI:
        if isinstance(func, CLI):
            return func
        return CLI(func)


class Option(CLIDecorator):
    """
    Decorator for defining both global and command options.

    :param name: Name of the option.
    :param kwargs: Keyword arguments to pass to the `add_argument` method of `argparse.ArgumentParser`.

    Example:
    ```Python
    @clipy.Command("command1", usage="usage of command1", description="description of command1" options=[
        clipy.Option("option1", help="an option", type=int, required=True)
    ])
    def func(command1: clipy.CommandDefinition):
        pass
    ```

    When used as a decorator, the `__call__` will return a `CLI` instance with the option registered as a global option.

    @clipy.Option("option1", help="an option", type=int, required=True)
    def func(option1: clipy.OptionDefinition):
        pass
    ```
    """

    def __init__(self, name: str, **kwargs):
        self.definition = OptionDefinition(name=name, kwargs=kwargs)

    @property
    def name(self) -> str:
        return self.definition.name

    @property
    def kwargs(self) -> dict:
        return self.definition.kwargs

    def __call__(self, func: Callable[..., Any]) -> CLI:
        wrapper: CLI = self.ensure_cli_wrapper(func)
        wrapper.register_global_option(self.definition)
        return wrapper


class Command(CLIDecorator):
    """
    Decorator for defining an argument parser command.

    :param name: Name of the command.
    :param usage: Usage string for the command.
    :param description: Description string for the command.
    :param options: List of `OptionDefinition` instances for the command. Default is an empty list.

    When used as a decorator, the `__call__` will return a `CLI` instance with the command registered.

    Example:
    ```Python
    @clipy.Command("command1", usage="usage of command1", description="description of command1" options=[
        clipy.Option("option1", help="an option", type=int, required=True)
    ])
    def func(command1: clipy.CommandDefinition):
        pass
    ```
    """

    def __init__(
        self,
        name: str,
        usage: str = None,
        description: str = None,
        options: List[OptionDefinition] = None,
    ):
        self.definition = CommandDefinition(
            name=name, usage=usage, description=description, options=options
        )

    def register_option(self, option: OptionDefinition):
        self.definition.register_option(option)

    def __call__(self, func: Callable[..., Any]) -> CLI:
        wrapper: CLI = self.ensure_cli_wrapper(func)
        wrapper.register_command(self.definition)
        return wrapper


class App(CLIDecorator):
    """
    Decorator for defining the main CLI application.

    :param usage: Usage string for the CLI application.
    :param description: Description string for the CLI application.

    When used as a decorator, the `__call__` will return a `CLI` instance with the usage and description set.

    Example:
    ```Python
    @clipy.App(usage="usage of app", description="description of app")
    def func():
        pass
    ```

    Full example:

    ```Python
    @clipy.App(usage="usage of app", description="description of app")
    @clipy.Option("option1", help="an option", type=int, required=True)
    @clipy.Command("command1", usage="usage of command1", description="description of command1" options=[
        clipy.Option("option1", help="an option", type=int, required=True)
    ])
    def func(command1: clipy.CommandDefinition):
        print(f"Command: {command.name}")
        print("Options:")
        for key, value in command.options.items():
            print(f"  {key}: {value}")
    ```
    """

    def __init__(self, usage: str = None, description: str = None):
        self.usage = usage
        self.description = description

    def __call__(self, func: Callable[..., Any]) -> CLI:
        wrapper: CLI = self.ensure_cli_wrapper(func)
        wrapper.usage = self.usage
        wrapper.description = self.description
        return wrapper
