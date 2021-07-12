import logging

from views.player import PlayerView
from views.tournament import TournamentView

from rich.console import Console
from rich.table import Table
from rich import box


class View:
    """Main View"""

    def __init__(self) -> None:
        self.view_player = PlayerView()
        self.view_tournament = TournamentView()
        self.console = Console()

    def displayMainMenu(self):
        """Display the Main Menu"""
        logging.info("View.displayMainMenu")
        table = Table(
            show_header=True,
            header_style="bold",
            title="-=[ SWESS ]=-\nGestionnaire de tournoi d'échecs",
            box=box.SIMPLE,
        )
        table.add_column("Menu principal")
        table.add_row("1. Afficher la liste complète des joueurs")
        table.add_row("2. Afficher l'historique des tournois")
        table.add_row("3. Afficher le classement")
        table.add_row("4. Ajouter un nouveau joueur")
        table.add_row("5. Créer un nouveau tournoi")
        table.add_row("6. Quitter")
        self.console.print(table)
