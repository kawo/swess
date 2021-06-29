# coding: utf-8

import tinydb
from tinydb.queries import where


class Database:

    db = tinydb.TinyDB("db.json", ensure_ascii=False)
    players_table = db.table("players")
    players_table.truncate()
    tournament_table = db.table("tournament")

    def entryExists(self, table: str, value: dict) -> bool:
        """check if entry exists before adding to db

        Args:
            table (str): table to check
            value (dict): value to check

        Returns:
            bool: return True if entry exist
        """
        if self.players_table.search(where("last_name") == value["last_name"]) and self.players_table.search(where("first_name") == value["first_name"]):
            print(f"Le joueur {value['last_name']} {value['first_name']} existe déjà !")
            return True
        else:
            return False

    def register(self, table: str, value: dict) -> None:
        """insert a value in a given table

        Args:
            table ([type]): table to insert to
            value ([type]): object to insert
        """
        self.value = value
        if table == "players":
            if self.entryExists("players", self.value) is False:
                self.players_table.insert(self.value)
        if table == "tournament":
            self.tournament_table.insert(self.value)
