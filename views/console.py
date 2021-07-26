"""Console View"""
import logging
import sys

from rich import box
from rich.console import Console
from rich.table import Table


class View:
    def __init__(self) -> None:
        self.console = Console()

    def printToUser(self, value):
        print_value = value
        console_print = self.console.print(print_value)  # type: ignore
        return console_print

    def askUser(self, value: str):
        question_value = value
        question = self.console.input(question_value)
        return question

    def displayMainMenu(self):
        """Display the Main Menu"""
        logging.info("View.displayMainMenu")
        table = Table(
            show_header=True,
            header_style="bold",
            title="-=[ SWESS ]=-\nChess Tournament Management",
            box=box.SIMPLE,
        )
        table.add_column("Main Menu")
        table.add_row("1. Display all players")
        table.add_row("2. Display tournaments logs")
        table.add_row("3. Display ranking")
        table.add_row("4. Create a new player")
        table.add_row("5. Create a new tournament")
        table.add_row("6. Quit")
        self.console.print(table)
        try:
            logging.info("Request user choice")
            user_choice = self.askUser("Type a number from menu: ")
            logging.info(f"User choice: {user_choice}")
            return user_choice
        except KeyboardInterrupt:
            self.printToUser("\n[bold red]You ended the program with CTRL+C![/bold red]")
            logging.info("Program ended by CTRL+C")
            return sys.exit()

    def displayAllPlayers(self, value) -> None:
        """display all recorded players"""

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
        return self.printToUser(table)

    def displaySortedByRating(self, value) -> None:
        """display all recorded players sorted by rating"""

        self.sorted_players = value
        table = Table(show_header=True, header_style="bold", title="\n-=[ SWESS ]=-\nPlayers Ranking", box=box.SIMPLE)
        table.add_column("Last Name")
        table.add_column("First Name")
        table.add_column("Gender")
        table.add_column("Birthday")
        table.add_column("Ranking")
        for player in self.sorted_players:
            table.add_row(
                player["last_name"],
                player["first_name"],
                player["gender"],
                player["birthday"],
                str(player["rating"]),
            )
        return self.printToUser(table)
