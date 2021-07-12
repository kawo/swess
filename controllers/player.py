import logging

from models.player import Player

from rich.console import Console


class PlayerController:
    def __init__(self) -> None:
        self.console = Console(color_system=None)

    def addPlayer(self):
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
        player = Player(first_name, last_name, birthday, gender, rating)
        if player:
            logging.info("Player successfully created!")
            return self.console.print(player)
        else:
            logging.error("Can not create player!")
