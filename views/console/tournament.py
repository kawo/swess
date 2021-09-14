"""Tournaments View"""
import logging

from rich import box
from rich.table import Table
from views.console.base import BaseView


class TournamentView(BaseView):
    def displayTournamentLogs(self, value):
        """Display all registered tournaments"""
        self.console.clear()
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
                tournament["end_date"],
                str(tournament["rounds_number"]),
                tournament["time_type"],
                tournament["description"],
            )
        self.printToUser(table, justify="center")
        self.printToUser("1. Choose Tournament")
        self.printToUser("2. Return to Main Menu")
        self.printToUser("\n")

    def displayNewTournament(self):
        """Form to add New Tournament"""
        self.console.clear()
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
        """Form to add players to new tournament"""
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

    def displayTournament(self, tournament, players) -> None:
        """display choosed tournament"""
        self.console.clear()
        tournament = tournament
        players = players
        table = Table(
            show_header=True, header_style="bold", title="\n-=[ SWESS ]=-\nTournament details", box=box.SIMPLE
        )
        table.add_column("Name")
        table.add_column("Location")
        table.add_column("Date")
        table.add_column("End Date")
        table.add_column("Rounds")
        table.add_column("Time Type")
        table.add_column("Description")
        table.add_row(
            tournament["name"],
            tournament["location"],
            tournament["date"],
            tournament["end_date"],
            str(tournament["rounds_number"]),
            tournament["time_type"],
            tournament["description"],
        )
        table.add_row("", "", "", "", "", "", "")
        table.add_row("", "", "", "Players list", "", "", "")
        table.add_row("", "", "", "", "", "", "")
        for player in players:
            table.add_row(
                "",
                player["first_name"],
                player["last_name"],
                player["gender"],
                player["birthday"],
                str(player["rating"]),
                "",
            )
        self.printToUser(table, justify="center")
        self.printToUser("1. Start/continue tournament")
        self.printToUser("2. Return to Main Menu")
        self.printToUser("\n")

    def displayFirstRound(self, players):
        """Display first round"""
        players = players
        self.printToUser("\n")
        table = Table(show_header=True, header_style="bold", title="Round 1", box=box.SIMPLE)
        table.add_column("Game 1", justify="center")
        table.add_column("Game 2", justify="center")
        table.add_column("Game 3", justify="center")
        table.add_column("Game 4", justify="center")
        table.add_row(
            f"{players[0][0]['first_name']} {players[0][0]['last_name']} ({players[0][0]['rating']})\nvs\n{players[0][1]['first_name']} {players[0][1]['last_name']} ({players[0][1]['rating']})",
            f"{players[1][0]['first_name']} {players[1][0]['last_name']} ({players[1][0]['rating']})\nvs\n{players[1][1]['first_name']} {players[1][1]['last_name']} ({players[1][1]['rating']})",
            f"{players[2][0]['first_name']} {players[2][0]['last_name']} ({players[2][0]['rating']})\nvs\n{players[2][1]['first_name']} {players[2][1]['last_name']} ({players[2][1]['rating']})",
            f"{players[3][0]['first_name']} {players[3][0]['last_name']} ({players[3][0]['rating']})\nvs\n{players[3][1]['first_name']} {players[3][1]['last_name']} ({players[3][1]['rating']})",
        )
        self.printToUser(table, justify="center")
        self.printToUser("1. Enter results")
        self.printToUser("2. End round")
        self.printToUser("3. Return to Main Menu")
        self.printToUser("\n")

    def displayRound(self, round, players, games: list = []):
        """Display rounds"""
        games = games
        round_number = round
        logging.info(f"displayRound: {round_number}")
        players = players
        logging.info(f"displayRound players list: {players}")
        self.printToUser("\n")
        table = Table(show_header=True, header_style="bold", title=f"Round {round_number}", box=box.SIMPLE)
        table.add_column(f"Game {games[0]}", justify="center")
        table.add_column(f"Game {games[1]}", justify="center")
        table.add_column(f"Game {games[2]}", justify="center")
        table.add_column(f"Game {games[3]}", justify="center")
        table.add_row(
            f"{players[0]['first_name']} {players[0]['last_name']} ({players[0]['score']})\nvs\n{players[1]['first_name']} {players[1]['last_name']} ({players[1]['score']})",
            f"{players[2]['first_name']} {players[2]['last_name']} ({players[2]['score']})\nvs\n{players[3]['first_name']} {players[3]['last_name']} ({players[3]['score']})",
            f"{players[4]['first_name']} {players[4]['last_name']} ({players[4]['score']})\nvs\n{players[5]['first_name']} {players[5]['last_name']} ({players[5]['score']})",
            f"{players[6]['first_name']} {players[6]['last_name']} ({players[6]['score']})\nvs\n{players[7]['first_name']} {players[7]['last_name']} ({players[7]['score']})",
        )
        self.printToUser(table, justify="center")
        self.printToUser("1. Enter results")
        self.printToUser("2. End round")
        self.printToUser("3. Return to Main Menu")
        self.printToUser("\n")

    def chooseGame(self):
        """Aske user to choose a game to enter restuls"""
        game_id = self.askUser("Enter results for which game? ")
        return game_id

    def showGame(self, players, game_id):
        """Show game details"""
        game_id = game_id
        players = players
        self.printToUser("\n")
        table = Table(show_header=True, header_style="bold", title=f"Game {game_id}", box=box.SIMPLE)
        table.add_column("Id", justify="center")
        table.add_column("Player", justify="center")
        table.add_column("Score", justify="center")
        table.add_column("Ranking", justify="center")
        for player in players:
            table.add_row(
                str(player["id"]),
                f"{player['first_name']} {player['last_name']}",
                str(player["score"]),
                str(player["rating"]),
            )
        self.printToUser(table, justify="center")

    def displayTournamentEnded(self, tournament, players):
        """Display Ended Tournament"""
        self.console.clear()
        tournament = tournament
        players = players
        table = Table(
            show_header=True, header_style="bold", title="\n-=[ SWESS ]=-\nTournament details", box=box.SIMPLE
        )
        table.add_column("Name", justify="center")
        table.add_column("Location", justify="center")
        table.add_column("Date", justify="center")
        table.add_column("End Date", justify="center")
        table.add_column("Rounds", justify="center")
        table.add_column("Time Type", justify="center")
        table.add_column("Description", justify="center")
        table.add_row(
            tournament["name"],
            tournament["location"],
            tournament["date"],
            tournament["end_date"],
            str(tournament["rounds_number"]),
            tournament["time_type"],
            tournament["description"],
        )
        table.add_row("", "", "", "", "", "", "")
        table.add_row("", "", "", "Players Ranking By Score", "", "", "")
        table.add_row("", "", "", "", "", "", "")
        for player in players:
            table.add_row(
                "",
                player["first_name"],
                player["last_name"],
                player["gender"],
                player["birthday"],
                str(player["score"]),
                "",
            )
        self.printToUser(table, justify="center")
        self.printToUser("1. Show Tournament's Rounds and Games")
        self.printToUser("2. Return to Main Menu")
        self.printToUser("\n")

    def displayEndedRound(self, round, players, games: list = []):
        """Display Ended Round"""
        games = games
        round_number = round
        logging.info(f"displayRound: {round_number}")
        players = players
        logging.info(f"displayRound players list: {players}")
        self.printToUser("\n")
        table = Table(show_header=True, header_style="bold", title=f"Round {round_number}", box=box.SIMPLE)
        table.add_column(f"Game {games[0]}", justify="center")
        table.add_column(f"Game {games[1]}", justify="center")
        table.add_column(f"Game {games[2]}", justify="center")
        table.add_column(f"Game {games[3]}", justify="center")
        table.add_row(
            f"{players[0]['first_name']} {players[0]['last_name']} ({players[0]['score']})\nvs\n{players[1]['first_name']} {players[1]['last_name']} ({players[1]['score']})",
            f"{players[2]['first_name']} {players[2]['last_name']} ({players[2]['score']})\nvs\n{players[3]['first_name']} {players[3]['last_name']} ({players[3]['score']})",
            f"{players[4]['first_name']} {players[4]['last_name']} ({players[4]['score']})\nvs\n{players[5]['first_name']} {players[5]['last_name']} ({players[5]['score']})",
            f"{players[6]['first_name']} {players[6]['last_name']} ({players[6]['score']})\nvs\n{players[7]['first_name']} {players[7]['last_name']} ({players[7]['score']})",
        )
        self.printToUser(table, justify="center")
        self.printToUser("1. Show Tournament's Rounds and Games")
        self.printToUser("2. Return to Main Menu")
        self.printToUser("\n")
