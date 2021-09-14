"""Player Model"""
import logging

from models.database import Database
from models.validator import Date, IntPositive, OneOf, String


class Player:

    first_name = String(minsize=3, maxsize=30, name="First Name")
    last_name = String(minsize=3, maxsize=30, name="Last Name")
    gender = OneOf("Gender", "M", "F")
    birthday = Date("Birthday", "%d/%m/%Y")
    rating = IntPositive("Ranking")

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

    def addToDb(self, value, serialize: bool = True) -> bool:
        """Add player to database

        Args:
            value (Player): player instance to add

        Returns:
            bool: return True if player is added to database
        """
        self.player = value
        self.serialize = serialize
        self.db = Database()
        if self.serialize:
            logging.info(f"serialize = {serialize}")
            self.insert_player = self.db.insertPlayer(self.player, True)
        else:
            logging.info(f"serialize = {serialize}")
            self.insert_player = self.db.insertPlayer(self.player, False)
        return self.insert_player

    def getAllPlayers(self):
        """get all the players from the database"""
        self.db = Database()
        all_players = self.db.getAll("players")
        return all_players

    def getPlayerById(self, value):
        """Get player by ID"""
        id = value
        self.db = Database()
        player = self.db.getPlayerById(id)
        return player

    def modifyRanking(self, id: int, ranking: int):
        """Modify player rating

        Args:
            id (int): player id
            ranking (int): player rating
        """
        id = id
        ranking = ranking
        self.db = Database()
        self.db.modifyRanking(id, ranking)

    def dummyData(self):
        """Dummy data for testing purpose"""
        players = [
            {"first_name": "Piers", "last_name": "Kelly", "gender": "M", "birthday": "10/09/1980", "rating": 1500},
            {"first_name": "Rose", "last_name": "Lawrence", "gender": "F", "birthday": "08/01/1984", "rating": 0},
            {"first_name": "Joseph", "last_name": "James", "gender": "M", "birthday": "23/04/1978", "rating": 1000},
            {"first_name": "Bernadette", "last_name": "Dyer", "gender": "F", "birthday": "01/11/1992", "rating": 2000},
            {"first_name": "Lisa", "last_name": "Mackenzie", "gender": "F", "birthday": "12/06/1987", "rating": 500},
            {"first_name": "Luke", "last_name": "Hill", "gender": "M", "birthday": "18/10/1990", "rating": 1800},
            {"first_name": "Jonathan", "last_name": "Bond", "gender": "M", "birthday": "28/12/1972", "rating": 2100},
            {"first_name": "Jason", "last_name": "Paterson", "gender": "M", "birthday": "20/01/1983", "rating": 1500},
            {"first_name": "Sonia", "last_name": "Davidson", "gender": "F", "birthday": "19/11/1986", "rating": 1200},
            {"first_name": "Stephen", "last_name": "McLean", "gender": "M", "birthday": "28/06/1996", "rating": 2800},
        ]
        self.db = Database()
        self.db.players_table.truncate()
        for player in players:
            logging.info(f"{player}")
            Player.addToDb(self, player, False)

    def __str__(self) -> str:
        return f"Player: {self.first_name} {self.last_name}, {self.gender} gender, born on {self.birthday} with a ranking of {self.rating}."
