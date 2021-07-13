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
        first_name = self.console.input("Entrez le prénom : ")
        logging.info(f"first_name = {first_name}")
        logging.info("Asking Last Name")
        last_name = self.console.input("Entrez le nom : ")
        logging.info(f"last_name = {last_name}")
        logging.info("Asking Birthday")
        birthday = self.console.input("Entrez la date d'anniversaire (jj/mm/aaaa) : ")
        logging.info(f"birthday = {birthday}")
        logging.info("Asking Gender")
        gender = self.console.input("Entrez le genre (M ou F) : ")
        logging.info(f"gender = {gender}")
        logging.info("Asking Rating")
        rating = self.console.input("Entrez le classement (optionnel) : ")
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
                    f"[bold green]Le joueur {first_name} {last_name}, du genre {gender}, né(e) le {birthday} avec un classement de {rating} a été ajouté dans la base de données ![/bold green]"
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
        show_all_players = Player.getAllPlayers(self)
        self.view.displayAllPlayers(show_all_players)
