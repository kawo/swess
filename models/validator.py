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
        try:
            if not isinstance(value, str):
                raise TypeError
        except TypeError:
            logging.error(f"{self.name} must be a str type! ({value!r})")
            return self.console.print(f"Le {self.name} doit être une chaîne de caractères !")
        try:
            if not value:
                raise ValueError
        except ValueError:
            logging.error(f"{self.name} can not be empty! ({value!r})")
            return self.console.print(f"[bold red]Le {self.name} ne peut pas être vide ![/bold red]")
        try:
            if self.minsize is not None and len(value) < self.minsize:
                raise ValueError
        except ValueError:
            logging.error(f"{self.name} can not be lower than {self.minsize}! ({value!r})")
            return self.console.print(
                f"[bold red]Le {self.name} ne peut pas être plus petit que {self.minsize!r} ![/bold red]"
            )
        try:
            if self.maxsize is not None and len(value) > self.maxsize:
                raise ValueError
        except ValueError:
            logging.error(f"{self.name} can not be lower than {self.maxsize}! ({value!r})")
            return self.console.print(
                f"[bold red]Le {self.name} ne peut pas être plus grand que {self.maxsize!r} ![/bold red]"
            )


class OneOf(Validator):
    def __init__(self, name, *options):
        self.name = name
        self.options = set(options)
        self.console = Console()

    def validate(self, value):
        try:
            if not value:
                raise ValueError
        except ValueError:
            logging.error(f"{self.name} can not be empty! ({value!r})")
            return self.console.print(f"[bold red]{self.name} ne peut pas être vide ![/bold red]")
        try:
            if value not in self.options:
                raise ValueError
        except ValueError:
            logging.error(f"{self.name} must be one of {self.options!r} ({value!r})")
            return self.console.print(f"[bold red]{self.name} doit faire parti de {self.options!r} ![/bold red]")


class Date(Validator):
    def __init__(self, name: str, format: str) -> None:
        self.name = name
        self.format = format
        self.console = Console()

    def validate(self, value: str):
        try:
            if not value:
                raise ValueError
        except ValueError:
            logging.error(f"{self.name} can not be empty! ({value!r})")
            return self.console.print(f"[bold red]{self.name} ne peut pas être vide ![/bold red]")
        try:
            datetime.strptime(value, self.format)
        except ValueError:
            logging.error(f"{self.name} must be in {self.format} ({value!r})")
            return self.console.print(
                f"[bold red]Le format de {self.name} ({value!r}) n'est pas valide ! Veuillez utiliser {self.format}[/bold red]"
            )
