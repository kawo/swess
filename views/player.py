from rich.console import Console
from rich.table import Table
from rich import box
from controllers.player import PlayerController


class PlayerView:

    def __init__(self) -> None:
        self.controller = PlayerController()
        self.console = Console()

    def displayAllPlayer(self) -> None:
        """display all recorded players"""
        table = Table(show_header=True, header_style="bold", title="-=[ SWESS ]=-\nListe complète des joueurs", box=box.SIMPLE)
        table.add_column("Id")
        table.add_column("Nom")
        table.add_column("Prénom")
        table.add_column("Anniversaire")
        table.add_column("Sexe")
        table.add_column("Classement")
        for player in self.controller.showAllPlayers():
            table.add_row(str(player.doc_id), player["last_name"], player["first_name"], player["birthday"], player["sex"], str(player["rating"]))
        self.console.print(table)

    def displayAddPlayer(self) -> None:
        """display the form to add a player"""
        new_player = self.controller.showAddPlayer()
        table = Table(show_header=True, header_style="bold", title="-=[ SWESS ]=-\nAjouter un joueur", box=box.SIMPLE)
        table.add_column("Nom")
        table.add_column("Prénom")
        table.add_column("Anniversaire")
        table.add_column("Sexe")
        table.add_column("Classement")
        table.add_row(new_player.last_name, new_player.first_name, new_player.birthday, new_player.sex, str(new_player.rating))
        self.console.print(table)
        self.console.print("Joueur ajouté !")
