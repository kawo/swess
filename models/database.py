import tinydb
from tinydb.queries import where
from rich.console import Console

import logging


class Database:
    def __init__(self) -> None:
        self.db = tinydb.TinyDB("db.json", ensure_ascii=False)
        self.players_table = self.db.table("players")
        self.tournament_table = self.db.table("tournament")
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

    def getAll(self):
        """Get all players from database"""
        logging.info("Getting all players from database...")
        players = self.players_table.all()
        return players
