from models.player import Player
from rich.console import Console


class PlayerController:

    def __init__(self) -> None:
        self.console = Console()

    def showAllPlayers(self):
        """ask all the players to the model"""
        show_all_players = Player.getAllPlayers(self)
        return show_all_players

    def showAddPlayer(self):
        """form to add a new player"""
        last_name = self.console.input("Entrez le Nom : ")
        first_name = self.console.input("Entrez le Prénom : ")
        birthday = self.console.input("Entrez l'anniversaire (jj/mm/aaaa) : ")
        sex = self.console.input("Entrez le Sexe (M ou F) : ")
        rating = self.console.input("Entrez le classement (optionel) : ")
        if rating:
            player = Player(last_name, first_name, birthday, sex, float(rating))
        else:
            player = Player(last_name, first_name, birthday, sex)
        player.registerPlayer(player)
        return player
