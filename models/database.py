import logging

import tinydb
from rich.console import Console
from tinydb.queries import where


class Database:
    def __init__(self) -> None:
        self.db = tinydb.TinyDB("db.json", ensure_ascii=False)
        self.players_table = self.db.table("players")
        self.tournament_table = self.db.table("tournaments")
        self.console = Console()

    def serializePlayer(self, value) -> dict:
        """serialize player for database insert

        Args:
            value (Player): player object.

        Returns:
            dict: return a player in dict format.
        """
        logging.info("Serializing player...")
        self.player = value
        serialized_player = {
            "first_name": self.player.first_name,
            "last_name": self.player.last_name,
            "gender": self.player.gender,
            "birthday": self.player.birthday,
            "rating": self.player.rating,
        }
        return serialized_player

    def checkPlayerExists(self, value: dict) -> bool:
        """check if player exists before adding to db

        Args:
            value (dict): value to check.

        Returns:
            bool: return True if entry exist.
        """
        logging.info("Checking if player already exist in database...")
        check = False
        last_name = value["last_name"]
        first_name = value["first_name"]
        if last_name != "" and first_name != "":
            if self.players_table.search(where("last_name") == last_name) and self.players_table.search(
                where("first_name") == first_name
            ):
                self.console.print(f"[bold red]Player {first_name} {last_name} already exist![/bold red]")
                logging.warning("Player already exist!")
                check = True
            else:
                logging.info("Player does not exist")
                check = False
        else:
            check = False
        return check

    def insertPlayer(self, value: object) -> bool:
        """insert a player to the database

        Args:
            value (Player): Player object to insert.
        """
        insert = False
        self.value = self.serializePlayer(value)
        if self.checkPlayerExists(self.value) is False:
            if self.players_table.insert(self.value):
                logging.info("Player inserted in database!")
                insert = True
            else:
                logging.warning("Player not inserted in database!")
                insert = False
        return insert

    def getAll(self, value: str):
        table = value
        if table == "players":
            logging.info("Getting all players from database...")
            result = self.players_table.all()
            return result
        if table == "tournaments":
            logging.info("Getting all tournaments from database...")
            result = self.tournament_table.all()
            return result
        else:
            logging.error(f"{table} table does not exists!")
            return None

    def serializeTournament(self, value) -> dict:
        """Serialize tournament for database insert

        Args:
            value (Tournament): tournament object.

        Returns:
            dict: return a tournament in dict format.
        """
        logging.info("Serializing tournament...")
        self.tournament = value
        serialized_tournament = {
            "name": self.tournament.name,
            "location": self.tournament.location,
            "rounds": self.tournament.rounds,
            "time_type": self.tournament.time_type,
            "description": self.tournament.description,
            "date": self.tournament.date,
            "games": self.tournament.games,
            "end_date": self.tournament.end_date,
            "players": self.tournament.players
        }
        return serialized_tournament

    def registerTournament(self, value: object) -> bool:
        """Register new tournament to database

        Args:
            value (Tournament): Tournament object to insert.
        """
        insert = False
        self.value = self.serializeTournament(value)
        if self.tournament_table.insert(self.value):
            logging.info("Tournament registered in database!")
            insert = True
        else:
            logging.warning("Tournament not registered in database!")
            insert = False
        logging.info(f"Insert: {insert}")
        return insert

    def addPlayers(self, value) -> bool:
        players = value
        players_exists = self.checkPlayerID(players)
        if players_exists:
            last_tournament = self.tournament_table.get(doc_id=len(self.db))
            self.tournament_table.update({'players': players}, doc_ids=last_tournament)
            return players_exists
        else:
            return players_exists

    def checkPlayerID(self, value) -> bool:
        players = value
        player_exists = True
        for player in players:
            logging.info(f"Checking Player ID: {player}")
            check_id = self.players_table.contains(doc_id=int(player))
            logging.info(f"{check_id}")
            if check_id:
                logging.info(f"Player ID {player} exists!")
            else:
                player_exists = False
                logging.error(f"Player ID {player} does not exists!")
        return player_exists
