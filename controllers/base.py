import logging
import sys

from views.base import View
from controllers.player import PlayerController


class Controller:
    """Main Controller"""

    def __init__(self) -> None:
        self.view = View()
        self.player_controller = PlayerController()

    def startApp(self):
        """Show Main Menu

        Returns:
            Display Main Menu
        """
        logging.info("Calling view.displayMainMenu")
        self.view.displayMainMenu()
        try:
            logging.info("Request user choice")
            user_choice = self.view.askUser("Type a number from menu: ")
            logging.info(f"User choice: {user_choice}")
            return self.mainMenuChoice(user_choice)
        except KeyboardInterrupt:
            self.view.printToUser("\n[bold red]You ended the program with CTRL+C![/bold red]")
            logging.info("Program ended by CTRL+C")

    def mainMenuChoice(self, choice: str):
        """Get user choice

        Args:
            choice (str): User choice from Main Menu.
        """
        choice = choice
        if choice == "":
            self.view.printToUser("[bold red]You must type a number![/bold red]\n")
            logging.warning("User input is empty")
            self.startApp()
        if choice == "1":
            logging.info("Calling view.displayAllPlayers()")
            self.player_controller.showAllPlayers()
        if choice == "3":
            logging.info("Calling controller player.sortPlayersByRating()")
            self.player_controller.sortPlayersByRating()
        if choice == "4":
            logging.info("Calling controller player.addPlayer()")
            self.player_controller.addPlayer()
        if choice == "6":
            self.view.printToUser("Byyye!")
            logging.info("Program terminated by the user")
            sys.exit()
