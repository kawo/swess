import logging

from models.player import Player
from views.base import View
from views.player import PlayerView


class PlayerController:
    def __init__(self) -> None:
        self.view = View()
        self.player_view = PlayerView()

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
        from controllers.base import Controller

        controller = Controller()
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
            controller.startApp()
        else:
            self.askRetryAddPlayer()

    def showAllPlayers(self):
        """ask model for all the players"""
        players = Player.getAllPlayers(self)
        self.player_view.displayAllPlayers(players)

    def sortPlayersByRating(self):
        """sort players by rating"""
        players = Player.getAllPlayers(self)
        players_sorted = sorted(players, key=lambda player: player["rating"], reverse=True)
        self.player_view.displaySortedByRating(players_sorted)
