import logging

from models.database import Database
from models.validator import Date, IntPositive, OneOf, String


class Tournament:

    name = String(minsize=3, maxsize=30, name="Tournament Name")
    location = String(minsize=3, maxsize=30, name="Location")
    description = String(minsize=10, maxsize=500, name="Description")
    time_type = OneOf("Time Type", "bullet", "blitz", "rapid")
    rounds = IntPositive("Rounds")
    date = Date("Date", "%d/%m/%Y")

    def __init__(self, name: str, location: str, time_type: str, description: str, date: str, rounds: int = 4, players: list[str] = [], games: list[str] = [], end_date: str = None) -> None:
        self.name = name
        self.location = location
        self.rounds = rounds
        self.time_type = time_type
        self.description = description
        self.date = date
        self.players = players
        self.games = games
        self.end_date = end_date

    def addToDb(self, value) -> bool:
        """Register tournament to database

        Args:
            value (Tournament): tournament instance to add

        Returns:
            bool: return True if tournament is registered to database
        """
        self.tournament = value
        self.db = Database()
        self.register_tournament = self.db.registerTournament(self.tournament)
        return self.register_tournament

    def getAllTournaments(self):
        """Get all registered tournaments from database"""
        self.db = Database()
        all_tournaments = self.db.getAll("tournaments")
        return all_tournaments

    def getAllOpenedTournaments(self):
        self.db = Database()
        opened_tournament = self.db.getOpenedTournaments()
        return opened_tournament

    def addPlayers(self, value):
        players = value
        self.db = Database()
        result = self.db.addPlayers(players)
        if result:
            logging.info("Players added to tournament!")
        else:
            logging.error("Players not added to tournaments!")

    def delTournaments(self):
        self.db = Database()
        self.db.tournament_table.truncate()
