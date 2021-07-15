import logging

from abc import ABC, abstractmethod
from datetime import datetime

from rich.console import Console


class Validator(ABC):
    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class String(Validator):
    def __init__(self, minsize: int, maxsize: int, name: str):
        """String validation

        Args:
            minsize (int): minimal size of the string
            maxsize (int): maximal size of the string
            name (str): display name of the string
        """
        self.minsize = minsize
        self.maxsize = maxsize
        self.name = name
        self.console = Console()

    def validate(self, value):
        if not isinstance(value, str):
            logging.error(f"{self.name} must be a str type! ({value!r})")
            raise TypeError(self.console.print(f"[bold red]{self.name} must be a str type! ({value!r})[/bold red]"))
        if not value:
            logging.error(f"{self.name} can not be empty! ({value!r})")
            raise ValueError(self.console.print(f"[bold red]{self.name} can not be empty![/bold red]"))
        if self.minsize is not None and len(value) < self.minsize:
            logging.error(f"{self.name} can not be lower than {self.minsize}! ({value!r})")
            raise ValueError(
                self.console.print(f"[bold red]{self.name} can not be lower than {self.minsize!r}![/bold red]")
            )
        if self.maxsize is not None and len(value) > self.maxsize:
            logging.error(f"{self.name} can not be lower than {self.maxsize}! ({value!r})")
            raise ValueError(
                self.console.print(f"[bold red]{self.name} can not be greater than {self.maxsize!r}![/bold red]")
            )


class OneOf(Validator):
    def __init__(self, name: str, *options) -> None:
        """Choices validation

        Args:
            name (str): display name of the list of choices
            *options (any): list of choices
        """
        self.name = name
        self.options = set(options)
        self.console = Console()

    def validate(self, value):
        if not value:
            logging.error(f"{self.name} can not be empty! ({value!r})")
            raise ValueError(self.console.print(f"[bold red]{self.name} can not be empty![/bold red]"))
        if value not in self.options:
            logging.error(f"{self.name} must be one of {self.options!r} ({value!r})")
            raise ValueError(self.console.print(f"[bold red]{self.name} must be one of {self.options!r}![/bold red]"))


class Date(Validator):
    def __init__(self, name: str, format: str) -> None:
        """Date validation

        Args:
            name (str): display name of the date
            format (str): date format
        """
        self.name = name
        self.format = format
        self.console = Console()
        self.date_ok = True

    def validate(self, value: str):
        if value is None:
            logging.error(f"{self.name} can not be empty! ({value!r})")
            self.date_ok = False
            raise ValueError(self.console.print(f"[bold red]{self.name} can not be empty![/bold red]"))
        try:
            self.date_ok = bool(datetime.strptime(value, self.format))
        except ValueError:
            self.date_ok = False

        if self.date_ok is False:
            logging.error(f"{self.name} must be in {self.format} ({value!r})")
            raise ValueError(self.console.print(f"[bold red]{self.name} must be in {self.format}![/bold red]"))


class IntPositive(Validator):
    def __init__(self, name: str) -> None:
        """Int positive validation

        Args:
            name (str): display name of the int to check
        """
        self.name = name
        self.console = Console()

    def validate(self, value: int):
        if not isinstance(value, int):
            logging.error(f"{self.name} must be an int ({value!r})")
            raise TypeError(self.console.print(f"[bold red]{self.name} must be an integer![/bold red]"))
        if value < 0:
            logging.error(f"{self.name} must be zero or positive ({value!r})")
            raise ValueError(self.console.print(f"[bold red]{self.name} must be zero or positive![/bold red]"))
