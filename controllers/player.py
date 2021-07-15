import logging

from models.player import Player
from views.player import PlayerView

from rich.console import Console


class PlayerController:
    def __init__(self) -> None:
        self.console = Console()
        self.view = PlayerView()

    def addPlayer(self) -> bool:
        """Create a new Player

        Returns:
            Player: a new created Player
        """
        logging.info("Asking First Name")
        first_name = self.console.input("First Name: ")
        logging.info(f"first_name = {first_name}")
        logging.info("Asking Last Name")
        last_name = self.console.input("Last Name: ")
        logging.info(f"last_name = {last_name}")
        logging.info("Asking Birthday")
        birthday = self.console.input("Birthday (dd/mm/yyyy): ")
        logging.info(f"birthday = {birthday}")
        logging.info("Asking Gender")
        gender = self.console.input("Gender (M or F): ")
        logging.info(f"gender = {gender}")
        logging.info("Asking Rating")
        rating = self.console.input("Ranking (optionnal): ")
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
                self.console.print(
                    f"[bold green]Player: {first_name} {last_name}, {gender} gender, born on {birthday} with a ranking of {rating} added in database![/bold green]"
                )
                return True
            else:
                logging.error("Can not insert player in database !")
                return False
        except (TypeError, ValueError):
            logging.error("Can not create player!")
            return False

    def showAllPlayers(self):
        """ask model for all the players"""
        players = Player.getAllPlayers(self)
        self.view.displayAllPlayers(players)

    def sortPlayersByRating(self):
        """sort players by rating"""
        players = Player.getAllPlayers(self)
        players_sorted = sorted(players, key=lambda player: player["rating"], reverse=True)
        self.view.displaySortedByRating(players_sorted)
