"""Console View"""
import logging

from rich import box
from rich.console import Console
from rich.table import Table


class BaseView:
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
        self.console.clear()
        table = Table(
            show_header=True,
            header_style="bold",
            title="-=[ SWESS ]=-\nChess Tournament Management",
            box=box.SIMPLE,
        )
        table.add_column("Main Menu")
        table.add_row("1. Display all players")
        table.add_row("2. Display ranking")
        table.add_row("3. Display tournaments logs")
        table.add_row("4. Show current opened tournaments")
        table.add_row("5. Create a new player")
        table.add_row("6. Create a new tournament")
        table.add_row("7. Quit")
        table.add_row("-- DEBUG --")
        table.add_row("8. Generate dummy players for testing")
        table.add_row("9. Delete ALL tournaments data")
        self.console.print(table)
        logging.info("Request user choice")
        user_choice = self.askUser("Type a number from menu: ")
        logging.info(f"User choice: {user_choice}")
        return user_choice

    def askReturnToMainMenu(self):
        """Ask user to return to Main Menu"""
        logging.info("Asking if user wants to return to Main Menu")
        ask = self.askUser("Return to Main Menu? (y/n): ")
        if ask == "":
            logging.warning("User input is empty")
            self.printToUser("You must answer with [Y]es or [N]o!")
            return self.askReturnToMainMenu()
        if ask == "y":
            logging.info("User said Yes")
            return True
        if ask == "n":
            logging.info("User said No")
            logging.info("Asking again...")
            return self.askReturnToMainMenu()
        else:
            return self.askReturnToMainMenu()
