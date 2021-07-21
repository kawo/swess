from views.base import View
from rich.console import Console
from rich.table import Table
from rich import box


class PlayerView(View):
    def __init__(self) -> None:
        self.console = Console()

    def displayAllPlayers(self, value) -> None:
        """display all recorded players"""

        self.players_list = value
        table = Table(
            show_header=True, header_style="bold", title="\n-=[ SWESS ]=-\nList of all players", box=box.SIMPLE
        )
        table.add_column("Id")
        table.add_column("Last Name")
        table.add_column("First Name")
        table.add_column("Gender")
        table.add_column("Birthday")
        table.add_column("Ranking")
        for player in self.players_list:
            table.add_row(
                str(player.doc_id),
                player["last_name"],
                player["first_name"],
                player["gender"],
                player["birthday"],
                str(player["rating"]),
            )
        self.printToUser(table)

    def displaySortedByRating(self, value) -> None:
        """display all recorded players sorted by rating"""

        self.sorted_players = value
        table = Table(show_header=True, header_style="bold", title="\n-=[ SWESS ]=-\nPlayers Ranking", box=box.SIMPLE)
        table.add_column("Last Name")
        table.add_column("First Name")
        table.add_column("Gender")
        table.add_column("Birthday")
        table.add_column("Ranking")
        for player in self.sorted_players:
            table.add_row(
                player["last_name"],
                player["first_name"],
                player["gender"],
                player["birthday"],
                str(player["rating"]),
            )
        self.printToUser(table)
