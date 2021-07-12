from models.validator import String, OneOf, Date


class Player:
    """Player Model"""

    first_name = String(minsize=3, maxsize=30, name="Prénom")
    last_name = String(minsize=3, maxsize=30, name="Nom")
    gender = OneOf("Genre", "M", "F")
    birthday = Date("Anniversaire", "%d/%m/%Y")

    def __init__(self, first_name: str, last_name: str, birthday: str, gender: str, rating: int = 0) -> None:
        """Player Object

        Args:
            first_name (str): First Name of the player.
            last_name (str): Last Name of the player.
            birthday (str): Birthday of the player (dd/mm/yyyy format).
            gender (str): Gender of the player (M or F).
            rating (int, optional): Rating of the player. Defaults to 0.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.gender = gender
        self.rating = rating

    def __str__(self) -> str:
        return f"Joueur {self.first_name} {self.last_name}, né(e) le {self.birthday}, de sexe {self.gender} et dont le classement est de {self.rating}."
