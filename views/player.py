from rich.console import Console
from rich.table import Table
from rich import box


class PlayerView:
    def __init__(self) -> None:
        self.console = Console()

    def displayAllPlayers(self, value) -> None:
        """display all recorded players"""

        self.players_list = value
        table = Table(
            show_header=True, header_style="bold", title="-=[ SWESS ]=-\nListe complète des joueurs", box=box.SIMPLE
        )
        table.add_column("Id")
        table.add_column("Nom")
        table.add_column("Prénom")
        table.add_column("Genre")
        table.add_column("Anniversaire")
        table.add_column("Classement")
        for player in self.players_list:
            table.add_row(
                str(player.doc_id),
                player["last_name"],
                player["first_name"],
                player["gender"],
                player["birthday"],
                str(player["rating"]),
            )
        self.console.print(table)
