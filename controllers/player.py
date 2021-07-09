from models.player import Player
from rich.console import Console


class PlayerController:
    def __init__(self) -> None:
        self.console = Console()

    def showAllPlayers(self):
        """ask model for all the players"""
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
            try:
                Player(last_name, first_name, birthday, sex, int(rating))
            except Exception as e:
                print(e)
        else:
            try:
                Player(last_name, first_name, birthday, sex)
            except Exception as e:
                print(e)

    def showAskAddPlayer(self):
        """ask user to retry adding player"""
        choice = self.console.input("Voulez-vous recommencer ? (o/n)")
        if choice == "o":
            self.view.displayAddPlayer()
        else:
            exit()

    def showMenuPlayer(self):
        """show menu for player view"""
        choice = self.console.input("Retourner au menu principal ? (o/n) : ")
        if choice == "o":
            print("ok")
        else:
            exit()
