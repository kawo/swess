"""Console View"""
import logging
import sys

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
