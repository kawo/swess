"""Players View"""
import logging

from rich import box
from rich.table import Table
from views.console.base import BaseView


class PlayerView(BaseView):
    def displayAllPlayers(self, value) -> None:
        """display all recorded players"""
        self.console.clear()
        self.players_list = value
        table = Table(
            show_header=True, header_style="bold", title="\n-=[ SWESS ]=-\nList of all players", box=box.SIMPLE
        )
        table.add_column("Id")
        table.add_column("Last Name")
        table.add_column("First Name")
        table.add_column("Gender")
        table.add_column("Birthday")
        table.add_column("Ranking")
        for player in self.players_list:
            table.add_row(
                str(player.doc_id),
                player["last_name"],
                player["first_name"],
                player["gender"],
                player["birthday"],
                str(player["rating"]),
            )
        self.printToUser(table, justify="center")
        self.printToUser("1. View/modify player")
        self.printToUser("2. Return to Main Menu")
        self.printToUser("\n")

    def displayPlayer(self, player) -> None:
        """display all recorded players"""
        self.console.clear()
        player = player
        table = Table(show_header=True, header_style="bold", title="\n-=[ SWESS ]=-\nPlayer details", box=box.SIMPLE)
        table.add_column("Last Name")
        table.add_column("First Name")
        table.add_column("Gender")
        table.add_column("Birthday")
        table.add_column("Ranking")
        table.add_row(
            player["last_name"],
            player["first_name"],
            player["gender"],
            player["birthday"],
            str(player["rating"]),
        )
        self.printToUser(table, justify="center")
        self.printToUser("1. Modify ranking")
        self.printToUser("2. Return to Main Menu")
        self.printToUser("\n")

    def askNewRanking(self):
        """ask user new ranking"""
        ranking = self.askUser("New ranking: ")
        return ranking

    def displaySortedByRating(self, value) -> None:
        """display all recorded players sorted by rating"""
        self.console.clear()
        self.sorted_players = value
        table = Table(show_header=True, header_style="bold", title="\n-=[ SWESS ]=-\nPlayers Ranking", box=box.SIMPLE)
        table.add_column("Id")
        table.add_column("Last Name")
        table.add_column("First Name")
        table.add_column("Gender")
        table.add_column("Birthday")
        table.add_column("Ranking")
        for player in self.sorted_players:
            table.add_row(
                str(player.doc_id),
                player["last_name"],
                player["first_name"],
                player["gender"],
                player["birthday"],
                str(player["rating"]),
            )
        self.printToUser(table, justify="center")
        self.printToUser("1. View/modify player")
        self.printToUser("2. Return to Main Menu")
        self.printToUser("\n")

    def displayAddPlayer(self) -> dict:
        """Create a new Player

        Returns:
            Player: a new created Player
        """
        self.console.clear()
        player = {}
        logging.info("Asking First Name")
        first_name = self.askUser("First Name: ")
        player["first_name"] = first_name
        logging.info(f"first_name = {first_name}")
        logging.info("Asking Last Name")
        last_name = self.askUser("Last Name: ")
        player["last_name"] = last_name
        logging.info(f"last_name = {last_name}")
        logging.info("Asking Birthday")
        birthday = self.askUser("Birthday (dd/mm/yyyy): ")
        player["birthday"] = birthday
        logging.info(f"birthday = {birthday}")
        logging.info("Asking Gender")
        gender = self.askUser("Gender (M or F): ")
        player["gender"] = gender
        logging.info(f"gender = {gender}")
        logging.info("Asking Rating")
        rating = self.askUser("Ranking (optional): ")
        player["rating"] = rating
        logging.info(f"rating = {rating}")
        logging.info("Trying to create Player instance...")
        return player

    def askRetryAddPlayer(self):
        """Ask user to retry Player creation"""
        logging.info("Asking if user wants to retry creating a player")
        ask = self.askUser("Retry? (y/n): ")
        if ask == "":
            logging.warning("User input is empty")
            self.printToUser("You must answer with [Y]es or [N]o!")
            return self.askRetryAddPlayer()
        if ask == "y":
            logging.info("User said Yes")
            return True
        if ask == "n":
            logging.info("User said No")
            logging.info("Returning to Main Menu...")
            return False
        else:
            self.askRetryAddPlayer()

    def playerAdded(self, value):
        first_name = value["first_name"]
        last_name = value["last_name"]
        gender = value["gender"]
        birthday = value["birthday"]
        rating = value["rating"]
        if rating:
            self.printToUser(
                f"[bold green]Player: {first_name} {last_name}, {gender} gender, born on {birthday} with a ranking of {rating} added in database![/bold green]"
            )
        else:
            self.printToUser(
                f"[bold green]Player: {first_name} {last_name}, {gender} gender, born on {birthday} with a ranking of 0 added in database![/bold green]"
            )
