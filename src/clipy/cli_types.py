import dataclasses
from typing import Any, Dict, List


@dataclasses.dataclass
class OptionDefinition:
    """
    Definition of a command option.

    Attributes:
    :param name: Name of the option.
    :param kwargs: Keyword arguments to pass to the `add_argument` method of `argparse.ArgumentParser`.
    """

    name: str
    kwargs: Dict[str, Any]


@dataclasses.dataclass
class CommandDefinition:
    """
    Definition of a command.

    Attributes:
    :param name: Name of the command.
    :param usage: Usage string for the command.
    :param description: Description string for the command.
    :param options: List of `OptionDefinition` instances for the command. Default is an empty list.
    """

    name: str
    usage: str = None
    description: str = None
    options: List[OptionDefinition] = None

    def __post_init__(self):
        if self.options is None:
            self.options = []

    def register_option(self, option: OptionDefinition):
        self.options.append(option)
