from abc import ABC, abstractmethod
from datetime import datetime


class Validator(ABC):
    """Abstract class to validate inputs"""

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
    """Check a string input

    Args:
        minsize (int): min size of string.
        maxsize (int): max size of string.
        name (str): display name of the string.
    """

    def __init__(self, minsize=None, maxsize=None, name=None) -> None:
        self.minsize = minsize
        self.maxsize = maxsize
        self.name = name

    def validate(self, value: str):
        try:
            if not isinstance(value, str):
                raise TypeError
        except TypeError:
            return print(f"Le {self.name} ne doit contenir que des caractères")
        try:
            if len(value) == 0:
                raise ValueError
        except ValueError:
            return print(f"Le {self.name} ne peut pas être vide")
        try:
            if self.minsize is not None and len(value) < self.minsize:
                raise ValueError
        except ValueError:
            return print(f"Le {self.name} ne peut pas être plus petit que {self.minsize} caractère(s)")
        try:
            if self.maxsize is not None and len(value) > self.maxsize:
                raise ValueError
        except ValueError:
            return print(f"Le {self.name} ne peut pas être plus long que {self.maxsize} caractère(s)")


class Choice(Validator):
    """Check a choice input

    Args:
        name (str): display name of the choice.
        *options (list): list of choices.
    """

    def __init__(self, name: str, *options) -> None:
        self.name = name
        self.options = set(options)

    def validate(self, value: str):
        value = str.upper(value)
        try:
            if value not in self.options:
                raise ValueError
        except ValueError:
            return print(f"Le {self.name} doit être l'une de ces options : {self.options}")


class Date(Validator):
    """Check a date input

    Args:
        name (str): display name of the date.
        format (str): date format.
    """

    def __init__(self, name: str, format: str) -> None:
        self.name = name
        self.format = format

    def validate(self, value: str):
        try:
            datetime.strptime(value, self.format)
        except ValueError:
            return print(f"Le format de {self.name} ({value}) n'est pas valide ! Veuillez utiliser {self.format}")


class FloatPositive(Validator):
    """Check if a float is zero or positive

    Args:
        name (str): display name of the float.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def validate(self, value: float):
        try:
            if not isinstance(value, float):
                raise TypeError
        except TypeError:
            return print(f"Le {self.name} doit être en décimal.")
        try:
            if value < 0:
                raise ValueError
        except ValueError:
            return print(f"{self.name} doit être positif ou nul !")
