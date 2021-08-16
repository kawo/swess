"""Main Controller for SWESS"""
import logging
import sys

from models.player import Player
from models.tournament import Tournament
from views.console.base import BaseView
from views.console.player import PlayerView
from views.console.tournament import TournamentView


class Controller:
    def __init__(self) -> None:
        self.base_view = BaseView()
        self.player_view = PlayerView()
        self.tournament_view = TournamentView()

    def startApp(self):
        """Show Main Menu

        Returns:
            Display Main Menu
        """
        logging.info("Calling view.displayMainMenu")
        choice = self.base_view.displayMainMenu()
        self.getMainMenuChoice(choice)

    def getMainMenuChoice(self, choice: str):
        """Get user choice

        Args:
            choice (str): User choice from Main Menu.
        """
        choice = choice
        if choice == "":
            self.base_view.printToUser("[bold red]You must type a number![/bold red]\n")
            logging.warning("User input is empty")
            return self.startApp()
        if choice == "1":
            logging.info("Displaying all players")
            return self.showAllPlayers()
        if choice == "2":
            logging.info("Displaying ranking")
            return self.sortPlayersByRating()
        if choice == "3":
            logging.info("Displaying tournaments logs")
            return self.showTournamentLogs()
        if choice == "4":
            logging.info("Displaying current opened tournaments")
            return self.showCurrentTournaments()
        if choice == "5":
            logging.info("Creating new player")
            return self.addPlayer()
        if choice == "6":
            logging.info("Creating new tournament")
            return self.createNewTournament()
        if choice == "7":
            self.base_view.printToUser("Byyye!")
            logging.info("Program terminated by the user")
            return sys.exit()
        else:
            logging.warning("User input is wrong")
            logging.warning("Returning to Main Menu...")
            return self.startApp()

    def returnToMainMenu(self):
        choice = self.base_view.askReturnToMainMenu()
        if choice:
            return self.startApp()

    def showTournamentLogs(self):
        """Ask model for all registered tournaments"""
        tournament = Tournament.getAllTournaments(self)
        self.tournament_view.displayTournamentLogs(tournament)
        return self.returnToMainMenu()

    def createNewTournament(self):
        tournament = self.tournament_view.displayNewTournament()
        name = tournament["name"]
        location = tournament["location"]
        date = tournament["date"]
        rounds = tournament["rounds"]
        time_type = tournament["time_type"]
        description = tournament["description"]
        try:
            if rounds:
                new_tournament = Tournament(name, location, time_type, description, date, int(rounds))
            else:
                new_tournament = Tournament(name, location, time_type, description, date)
            logging.info("Tournament successfully created!")
            logging.info("Trying to register tournament to database...")
            if new_tournament.addToDb(new_tournament):
                logging.info("Tournament successfully registered in database!")
                return self.tournament_view.tournamentAdded(tournament)
            else:
                logging.error("Can not register tournament in database!")
                retry = self.tournament_view.askRetryNewTournament()
                if retry:
                    return self.createNewTournament()
                else:
                    return self.startApp()
        except (TypeError, ValueError):
            logging.error("Can not create tournament!")
            retry = self.tournament_view.askRetryNewTournament()
            if retry:
                return self.createNewTournament()
            else:
                return self.startApp()

    def addPlayer(self):
        player = self.player_view.displayAddPlayer()
        first_name = player["first_name"]
        last_name = player["last_name"]
        birthday = player["birthday"]
        gender = player["gender"]
        rating = player["rating"]
        try:
            if rating:
                new_player = Player(first_name, last_name, birthday, gender, int(rating))
            else:
                new_player = Player(first_name, last_name, birthday, gender)
            logging.info("Player successfully created!")
            logging.info("Trying to add player to database...")
            if new_player.addToDb(new_player):
                logging.info("Player successfully inserted in database!")
                return self.player_view.playerAdded(player)
            else:
                logging.error("Can not insert player in database!")
                retry = self.player_view.askRetryAddPlayer()
                if retry:
                    return self.addPlayer()
                else:
                    return self.startApp()
        except (TypeError, ValueError):
            logging.error("Can not create player!")
            retry = self.player_view.askRetryAddPlayer()
            if retry:
                return self.addPlayer()
            else:
                return self.startApp()

    def showAllPlayers(self):
        """ask model for all the players"""
        players = Player.getAllPlayers(self)
        self.player_view.displayAllPlayers(players)
        return self.returnToMainMenu()

    def sortPlayersByRating(self):
        """sort players by rating"""
        players = Player.getAllPlayers(self)
        players_sorted = sorted(players, key=lambda player: player["rating"], reverse=True)
        self.player_view.displaySortedByRating(players_sorted)
        return self.returnToMainMenu()

    def showCurrentTournaments(self):
        pass
