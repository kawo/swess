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
    def __init__(self, minsize=None, maxsize=None, name=None):
        self.minsize = minsize
        self.maxsize = maxsize
        self.name = name
        self.console = Console()

    def validate(self, value):
        if not isinstance(value, str):
            self.console.print(f"Le {self.name} doit être une chaîne de caractères !")
            raise TypeError(logging.error(f"{self.name} must be a str type! ({value!r})"))
        if not value:
            self.console.print(f"[bold red]Le {self.name} ne peut pas être vide ![/bold red]")
            raise ValueError(logging.error(f"{self.name} can not be empty! ({value!r})"))
        if self.minsize is not None and len(value) < self.minsize:
            self.console.print(
                f"[bold red]Le {self.name} ne peut pas être plus petit que {self.minsize!r} ![/bold red]"
            )
            raise ValueError(logging.error(f"{self.name} can not be lower than {self.minsize}! ({value!r})"))
        if self.maxsize is not None and len(value) > self.maxsize:
            self.console.print(
                f"[bold red]Le {self.name} ne peut pas être plus grand que {self.maxsize!r} ![/bold red]"
            )
            raise ValueError(logging.error(f"{self.name} can not be lower than {self.maxsize}! ({value!r})"))


class OneOf(Validator):
    def __init__(self, name, *options):
        self.name = name
        self.options = set(options)
        self.console = Console()

    def validate(self, value):
        if not value:
            self.console.print(f"[bold red]{self.name} ne peut pas être vide ![/bold red]")
            raise ValueError(logging.error(f"{self.name} can not be empty! ({value!r})"))
        if value not in self.options:
            self.console.print(f"[bold red]{self.name} doit faire parti de {self.options!r} ![/bold red]")
            raise ValueError(logging.error(f"{self.name} must be one of {self.options!r} ({value!r})"))


class Date(Validator):
    def __init__(self, name: str, format: str) -> None:
        self.name = name
        self.format = format
        self.console = Console()

    def validate(self, value: str):
        if value is None:
            self.console.print(f"[bold red]{self.name} ne peut pas être vide ![/bold red]")
            raise ValueError(logging.error(f"{self.name} can not be empty! ({value!r})"))
        date_ok = True
        try:
            date_ok = bool(datetime.strptime(value, self.format))
        except ValueError:
            date_ok = False

        if date_ok is False:
            self.console.print(
                f"[bold red]Le format de {self.name} ({value!r}) n'est pas valide ! Veuillez utiliser {self.format}[/bold red]"
            )
            raise ValueError(logging.error(f"{self.name} must be in {self.format} ({value!r})"))


class IntPositive(Validator):
    def __init__(self, name: str) -> None:
        self.name = name
        self.console = Console()

    def validate(self, value: int):
        if not isinstance(value, int):
            self.console.print(f"Le {self.name} doit être un nombre entier.")
            raise TypeError(logging.error(f"{self.name} must be an int"))
        if value < 0:
            self.console.print(f"{self.name} doit être positif ou nul !")
            raise ValueError(logging.error(f"{self.name} must be zero or positive ({value!r})"))
