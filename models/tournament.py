from models.database import Database
from models.validator import IntPositive, OneOf, String


class Tournament:

    name = String(minsize=3, maxsize=30, name="Tournament Name")
    location = String(minsize=3, maxsize=30, name="Location")
    description = String(minsize=10, maxsize=500, name="Description")
    time_type = OneOf("Time Type", "bullet", "blitz", "rapid")
    rounds = IntPositive("Rounds")

    def __init__(self, name: str, location: str, time_type: str, description: str, rounds: int = 4) -> None:
        self.name = name
        self.location = location
        self.rounds = rounds
        self.time_type = time_type
        self.description = description

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
