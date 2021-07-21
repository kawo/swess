import logging

from rich.console import Console
from rich.table import Table
from rich import box


class View:
    """Main View"""

    def __init__(self) -> None:
        self.console = Console()

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

    def printToUser(self, value):
        print_value = value
        console_print = self.console.print(print_value)  # type: ignore
        return console_print

    def askUser(self, value: str):
        question_value = value
        question = self.console.input(question_value)
        return question
