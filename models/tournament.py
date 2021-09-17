"""Tournament Model"""
import logging

from models.database import Database
from models.validator import Date, IntPositive, OneOf, String


class Tournament:

    name = String(minsize=3, maxsize=30, name="Tournament Name")
    location = String(minsize=3, maxsize=30, name="Location")
    description = String(minsize=10, maxsize=500, name="Description")
    time_type = OneOf("Time Type", "bullet", "blitz", "rapid")
    rounds_number = IntPositive("Rounds")
    date = Date("Date", "%d/%m/%Y")

    def __init__(
        self,
        name: str,
        location: str,
        time_type: str,
        description: str,
        date: str,
        rounds_number: int = 4,
        players: list[str] = [],
        rounds: list[int] = [],
        end_date: str = None,
    ) -> None:
        self.name = name
        self.location = location
        self.rounds_number = rounds_number
        self.time_type = time_type
        self.description = description
        self.date = date
        self.players = players
        self.rounds = rounds
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

    def registerRoundToTournament(self, round, id):
        """Register new round to tournament

        Args:
            round int: round id
            id int: tournament id
        """
        round = round
        tournament_id = id
        self.db = Database()
        self.db.registerRound(round, tournament_id)

    def getAllTournaments(self):
        """Get all registered tournaments from database"""
        self.db = Database()
        all_tournaments = self.db.getAll("tournaments")
        return all_tournaments

    def getAllOpenedTournaments(self):
        """Get all opened tournaments"""
        self.db = Database()
        opened_tournament = self.db.getOpenedTournaments()
        return opened_tournament

    def addPlayers(self, value):
        """Add players to tournament"""
        players = value
        self.db = Database()
        result = self.db.addPlayers(players)
        if result:
            logging.info("Players added to tournament!")
        else:
            logging.error("Players not added to tournaments!")

    def getTournamentById(self, value):
        """Get tournament details from ID

        Args:
            value int: tournament id

        Returns:
            list: tournament data
        """
        id = value
        self.db = Database()
        tournament = self.db.getTournamentById(id)
        return tournament

    def getPreviousRound(self, tournament):
        """Get previous round"""
        tournament_id = tournament
        tournament = Tournament.getTournamentById(self, tournament_id)
        previous_round = len(tournament["rounds"])
        return previous_round

    def checkRoundEndTime(self, tournament_id) -> bool:
        """Check if a round is ended

        Args:
            tournament_id (int): tournament id

        Returns:
            bool: True if round is ended
        """
        tournament_id = tournament_id
        result = self.db.checkRoundEndTime(tournament_id)
        return result

    def delTournaments(self):
        """Delete all tournaments data"""
        self.db = Database()
        self.db.tournament_table.truncate()
        self.db.rounds_table.truncate()
        self.db.games_table.truncate()
        self.db.paired_players.truncate()

    def endTournament(self, tournament_id):
        """End tournament"""
        tournament_id = tournament_id
        self.db = Database()
        return self.db.endTournament(tournament_id)
