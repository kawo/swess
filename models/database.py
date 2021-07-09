import tinydb
from tinydb.queries import where
from rich.console import Console


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
        check = False
        last_name = value["last_name"]
        first_name = value["first_name"]
        if table == "players":
            if last_name != "" and first_name != "":
                if self.players_table.search(where("last_name") == last_name) and self.players_table.search(
                    where("first_name") == first_name
                ):
                    self.console.print(f"Le joueur {last_name} {first_name} existe déjà !")
                    check = True
                else:
                    check = False
        else:
            check = False
        return check

    def insertPlayer(self, value) -> None:
        """insert a player to the database

        Args:
            value (Player): Player object to insert.
        """
        self.value = self.serializePlayer(value)
        if self.entryExists("players", self.value) is False:
            self.players_table.insert(self.value)
