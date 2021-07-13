from models.validator import String, OneOf, Date, IntPositive
from models.database import Database


class Player:

    first_name = String(minsize=3, maxsize=30, name="Prénom")
    last_name = String(minsize=3, maxsize=30, name="Nom")
    gender = OneOf("Genre", "M", "F")
    birthday = Date("Anniversaire", "%d/%m/%Y")
    rating = IntPositive("Classement")

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

    def addToDb(self, value) -> bool:
        self.player = value
        self.db = Database()
        self.insert_player = self.db.insertPlayer(self.player)
        return self.insert_player

    def getAllPlayers(self):
        """get all the players from the database"""
        self.db = Database()
        all_players = self.db.getAll()
        return all_players

    def modifyFirstName(self, value: str):
        pass

    def modifyLastName(self, value: str):
        pass

    def modifyBirthday(self, value: str):
        pass

    def modifyGender(self, value: str):
        pass

    def modifyRating(self, value: int):
        pass

    def delete(self, value: int):
        pass

    def __str__(self) -> str:
        return f"Joueur {self.first_name} {self.last_name}, du genre {self.gender}, né(e) le {self.birthday} avec un classement de {self.rating}."
