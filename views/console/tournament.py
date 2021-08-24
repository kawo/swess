import logging

from rich import box
from rich.table import Table
from views.console.base import BaseView


class TournamentView(BaseView):
    def displayTournamentLogs(self, value):
        """Display all registered tournaments"""

        self.tournaments_list = value
        table = Table(
            show_header=True, header_style="bold", title="\n-=[ SWESS ]=-\nList of all tournaments", box=box.SIMPLE
        )
        table.add_column("Id")
        table.add_column("Name")
        table.add_column("Location")
        table.add_column("Date")
        table.add_column("End Date")
        table.add_column("Rounds")
        table.add_column("Time Type")
        table.add_column("Description")
        for tournament in self.tournaments_list:
            table.add_row(
                str(tournament.doc_id),
                tournament["name"],
                tournament["location"],
                tournament["date"],
                tournament['end_date'],
                str(tournament["rounds"]),
                tournament["time_type"],
                tournament["description"],
            )
        return self.printToUser(table)

    def displayNewTournament(self):
        tournament = {}
        logging.info("Asking for Tournament Name")
        name = self.askUser("Tournament Name: ")
        tournament["name"] = name
        logging.info(f"name = {name}")
        logging.info("Asking Location")
        location = self.askUser("Location: ")
        tournament["location"] = location
        logging.info(f"location = {location}")
        logging.info("Asking Date")
        date = self.askUser("Date (dd/mm/yyyy): ")
        tournament["date"] = date
        logging.info(f"date = {date}")
        logging.info("Asking Round Numbers")
        rounds = self.askUser("Number of rounds (default: 4): ")
        tournament["rounds"] = rounds
        logging.info(f"rounds = {rounds}")
        logging.info("Asking Time Type")
        time_type = self.askUser("Time Type (bullet, blitz or rapid): ")
        tournament["time_type"] = time_type
        logging.info(f"time_type = {time_type}")
        logging.info("Asking Description")
        description = self.askUser("Description: ")
        tournament["description"] = description
        logging.info(f"description = {description}")
        logging.info("Trying to create Tournament instance...")
        return tournament

    def addPlayers(self):
        players = []
        logging.info("Asking for players list")
        self.printToUser("Add 8 players:")
        for i in range(8):
            player = self.askUser(f"Player {i+1}: ")
            if player == "":
                self.printToUser("[bold red]You must enter an ID![/bold red]")
                return self.addPlayers()
            else:
                players.append(player)
        if any(players.count(player) > 1 for player in players):
            logging.error("Duplicates found in players!")
            self.printToUser("[bold red]You can not have duplicate players![/bold red]")
            return self.addPlayers()
        logging.info(f"players = {players}")
        return players

    def askRetryNewTournament(self):
        """Ask user to retry Tournament creation"""
        logging.info("Asking if user wants to retry creating a tournament")
        ask = self.askUser("Retry? (y/n): ")
        if ask == "":
            logging.warning("User input is empty")
            self.printToUser("You must answer with [Y]es or [N]o!")
            return self.askRetryNewTournament()
        if ask == "y":
            logging.info("User said Yes")
            return True
        if ask == "n":
            logging.info("User said No")
            logging.info("Returning to Main Menu...")
            return False
        else:
            self.askRetryNewTournament()

    def tournamentAdded(self, value):
        name = value["name"]
        location = value["location"]
        date = value["date"]
        rounds = value["rounds"]
        time_type = value["time_type"]
        description = value["description"]
        if rounds:
            self.printToUser(f"[green]Tournament Name: {name!r}\nLocation: {location!r}\nDate: {date!r}\nRounds: {rounds!r}\nTime Type: {time_type!r}\nDescription: {description!r}[/green]\n[bold green]Registered in database![/bold green]")
        else:
            self.printToUser(f"[green]Tournament Name: {name!r}\nLocation: {location!r}\nDate: {date!r}\nRounds: '4'\nTime Type: {time_type!r}\nDescription: {description!r}[/green]\n[bold green]Registered in database![/bold green]")
