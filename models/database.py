# coding: utf-8

import tinydb
from tinydb.queries import where


class Database:

    db = tinydb.TinyDB("db.json", ensure_ascii=False)
    players_table = db.table("players")
    tournament_table = db.table("tournament")

    def serializePlayer(self, value) -> dict:
        """serialize player for database insert

        Args:
            value (Player): player object.

        Returns:
            dict: return a player in dict format.
        """
        self.player = value
        serialized_player = {
            "last_name": self.player.last_name,
            "first_name": self.player.first_name,
            "sex": self.player.sex,
            "rating": self.player.rating,
            "birthday": self.player.birthday,
        }
        return serialized_player

    def entryExists(self, table: str, value: dict) -> bool:
        """check if entry exists before adding to db

        Args:
            table (str): table to check.
            value (dict): value to check.

        Returns:
            bool: return True if entry exist.
        """
        if table == "players":
            if value["last_name"] != "" and value["first_name"] != "":
                if self.players_table.search(where("last_name") == value["last_name"]) and self.players_table.search(where("first_name") == value["first_name"]):
                    print(f"Le joueur {value['last_name']} {value['first_name']} existe déjà !")
                    return True
                else:
                    return False
        else:
            return False

    def insertPlayer(self, value) -> None:
        """insert a player to the database

        Args:
            value (Player): Player object to insert.
        """
        self.value = self.serializePlayer(value)
        if self.entryExists("players", self.value) is False:
            self.players_table.insert(self.value)
