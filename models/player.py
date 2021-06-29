from models.validator import Choice, Date, FloatPositive, String
from models.database import Database


class Player:
    """A player of chess tournament

    Args:
        last_name (str): last name.
        first_name (str): first name.
        birthday (str): date of birth.
        sex (str): sex (M or F).
        rating (int, optional): rating of player. Defaults to 0.0.
    """

    last_name = String(minsize=3, maxsize=30, name="Nom")
    first_name = String(minsize=3, maxsize=30, name="Prénom")
    sex = Choice("Sexe", "M", "F")
    birthday = Date("Anniversaire", "%d/%m/%Y")
    rating = FloatPositive("Classement")

    def __init__(self, last_name: str, first_name: str, birthday: str, sex: str, rating=0.0) -> None:
        self.last_name = last_name
        self.first_name = first_name
        self.sex = sex
        self.rating = rating
        self.birthday = birthday

    def serializePlayer(self, Player) -> dict:
        """serialize player for database insert

        Args:
            Player ([obj]): player object

        Returns:
            [dict]: return a player in dict format
        """
        self.player = Player
        serialized_player = {
            "last_name": self.player.last_name,
            "first_name": self.player.first_name,
            "sex": self.player.sex,
            "rating": self.player.rating,
            "birthday": self.player.birthday,
        }
        return serialized_player

    def addPlayer(self, Player: object) -> None:
        """add a player to the database

        Args:
            Player ([obj]): player object
        """
        self.player = self.serializePlayer(Player)
        player_db = Database()
        player_db.register("players", self.player)

    def __str__(self) -> str:
        return f"- Joueur -\nNom : {self.last_name}\nPrénom : {self.first_name}\nSexe : {str.upper(self.sex)}\nAnniversaire : {self.birthday}\nClassement : {self.rating}"
