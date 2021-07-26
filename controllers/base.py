"""Main Controller for SWESS"""
import logging
import sys

from models.player import Player
from views.console import View


class Controller:
    def __init__(self) -> None:
        self.view = View()

    def startApp(self):
        """Show Main Menu

        Returns:
            Display Main Menu
        """
        logging.info("Calling view.displayMainMenu")
        choice = self.view.displayMainMenu()
        self.getMainMenuChoice(choice)

    def getMainMenuChoice(self, choice: str):
        """Get user choice

        Args:
            choice (str): User choice from Main Menu.
        """
        choice = choice
        if choice == "":
            self.view.printToUser("[bold red]You must type a number![/bold red]\n")
            logging.warning("User input is empty")
            return self.startApp()
        if choice == "1":
            logging.info("Calling view.displayAllPlayers()")
            return self.showAllPlayers()
        if choice == "3":
            logging.info("Calling controller player.sortPlayersByRating()")
            return self.sortPlayersByRating()
        if choice == "4":
            logging.info("Calling controller player.addPlayer()")
            return self.addPlayer()
        if choice == "6":
            self.view.printToUser("Byyye!")
            logging.info("Program terminated by the user")
            return sys.exit()
        else:
            logging.warning("User input is wrong")
            logging.warning("Returning to Main Menu...")
            return self.startApp()

    def addPlayer(self):
        """Create a new Player

        Returns:
            Player: a new created Player
        """
        logging.info("Asking First Name")
        first_name = self.view.askUser("First Name: ")
        logging.info(f"first_name = {first_name}")
        logging.info("Asking Last Name")
        last_name = self.view.askUser("Last Name: ")
        logging.info(f"last_name = {last_name}")
        logging.info("Asking Birthday")
        birthday = self.view.askUser("Birthday (dd/mm/yyyy): ")
        logging.info(f"birthday = {birthday}")
        logging.info("Asking Gender")
        gender = self.view.askUser("Gender (M or F): ")
        logging.info(f"gender = {gender}")
        logging.info("Asking Rating")
        rating = self.view.askUser("Ranking (optional): ")
        logging.info(f"rating = {rating}")
        logging.info("Trying to create Player instance...")
        try:
            if rating:
                new_player = Player(first_name, last_name, birthday, gender, int(rating))
            else:
                new_player = Player(first_name, last_name, birthday, gender)
            logging.info("Player successfully created!")
            logging.info("Trying to add player to database...")
            if new_player.addToDb(new_player):
                logging.info("Player successfully inserted in database!")
                if rating:
                    self.view.printToUser(
                        f"[bold green]Player: {first_name} {last_name}, {gender} gender, born on {birthday} with a ranking of {rating} added in database![/bold green]"
                    )
                else:
                    self.view.printToUser(
                        f"[bold green]Player: {first_name} {last_name}, {gender} gender, born on {birthday} with a ranking of 0 added in database![/bold green]"
                    )
            else:
                logging.error("Can not insert player in database !")
                return self.askRetryAddPlayer()
        except (TypeError, ValueError):
            logging.error("Can not create player!")
            return self.askRetryAddPlayer()

    def askRetryAddPlayer(self):
        """Ask user to retry Player creation"""
        logging.info("Asking if user wants to retry creating a player")
        ask = self.view.askUser("Retry? (y/n): ")
        if ask == "":
            logging.warning("User input is empty")
            self.view.printToUser("You must answer with [Y]es or [N]o!")
            self.askRetryAddPlayer()
        if ask == "y":
            logging.info("User said Yes")
            new_player = self.addPlayer()
            if new_player is False:
                self.askRetryAddPlayer()
        if ask == "n":
            logging.info("User said No")
            logging.info("Returning to Main Menu...")
            self.view.printToUser("\n")
            self.startApp()
        else:
            self.askRetryAddPlayer()

    def askReturnToMainMenu(self):
        """Ask user to return to Main Menu"""
        logging.info("Asking if user wants to return to Main Menu")
        ask = self.view.askUser("Return to Main Menu? (y/n): ")
        if ask == "":
            logging.warning("User input is empty")
            self.view.printToUser("You must answer with [Y]es or [N]o!")
            return self.askReturnToMainMenu()
        if ask == "y":
            logging.info("User said Yes")
            return self.startApp()
        if ask == "n":
            logging.info("User said No")
            logging.info("Asking again...")
            return self.askReturnToMainMenu()
        else:
            return self.askReturnToMainMenu()

    def showAllPlayers(self):
        """ask model for all the players"""
        players = Player.getAllPlayers(self)
        self.view.displayAllPlayers(players)
        return self.askReturnToMainMenu()

    def sortPlayersByRating(self):
        """sort players by rating"""
        players = Player.getAllPlayers(self)
        players_sorted = sorted(players, key=lambda player: player["rating"], reverse=True)
        self.view.displaySortedByRating(players_sorted)
        return self.askReturnToMainMenu()
