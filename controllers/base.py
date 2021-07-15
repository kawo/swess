import logging
import sys

from controllers.player import PlayerController
from controllers.tournament import TournamentController
from controllers.round import RoundController
from controllers.match import MatchController

from views.base import View

from rich.console import Console


class Controller:
    """Main Controller"""

    def __init__(self) -> None:
        self.controller_player = PlayerController()
        self.controller_tournament = TournamentController()
        self.controller_round = RoundController()
        self.controller_match = MatchController()
        self.view = View()
        self.console = Console()

    def startApp(self):
        """Show Main Menu

        Returns:
            Display Main Menu
        """
        logging.info("Calling view.displayMainMenu")
        self.view.displayMainMenu()
        try:
            logging.info("Request user choice")
            user_choice = self.console.input("Type a number from menu : ")
            logging.info(f"User choice: {user_choice}")
            return self.mainMenuChoice(user_choice)
        except KeyboardInterrupt:
            self.console.print("\n[bold red]You ended the program with CTRL+C![/bold red]")
            logging.info("Program ended by CTRL+C")

    def mainMenuChoice(self, choice: str):
        """Get user choice

        Args:
            choice (str): User choice from Main Menu.
        """
        choice = choice
        if choice == "":
            self.console.print("[bold red]You must type a number![/bold red]\n")
            logging.warning("User input is empty")
            self.startApp()
        if choice == "1":
            logging.info("Calling view.displayAllPlayers()")
            self.controller_player.showAllPlayers()
        if choice == "3":
            logging.info("Calling controller player.sortPlayersByRating()")
            self.controller_player.sortPlayersByRating()
        if choice == "4":
            logging.info("Calling controller player.addPlayer()")
            new_player = self.controller_player.addPlayer()
            if new_player is False:
                self.askRetry()
        if choice == "6":
            self.console.print("Byyye!")
            logging.info("Program terminated by the user")
            sys.exit()

    def askRetry(self):
        """Ask user to retry Player creation"""
        logging.info("Asking if user wants to retry creating a player")
        ask = self.console.input("Retry? (y/n) : ")
        if ask == "":
            logging.warning("User input is empty")
            self.console.print("You must answer with [Y]es or [N]o!")
            self.askRetry()
        if ask == "y":
            logging.info("User said Yes")
            new_player = self.controller_player.addPlayer()
            if new_player is False:
                self.askRetry()
        if ask == "n":
            logging.info("User said No")
            logging.info("Returning to Main Menu...")
            self.startApp()
        else:
            self.askRetry()
