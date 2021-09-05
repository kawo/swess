"""Main Controller for SWESS"""
import logging
import sys

from models.player import Player
from models.round import Round
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
        if choice == "8":
            logging.info("Generating dummy data for testing purpose...")
            return self.generateDummyData()
        if choice == "9":
            logging.info("Deleting ALL tournaments data...")
            return self.deleteAllTournaments()
        else:
            logging.warning("User input is wrong")
            logging.warning("Returning to Main Menu...")
            return self.startApp()

    def returnToMainMenu(self):
        choice = self.base_view.askReturnToMainMenu()
        if choice:
            return self.startApp()

    def choosePlayer(self):
        choice = self.base_view.askPlayerId()
        if choice:
            player = Player.getPlayerById(self, choice)
            self.player_view.displayPlayer(player)
            return self.playerMenuChoice(choice)

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
                return self.addPlayersToTournament()
            else:
                logging.error("Can not register tournament in database!")
                retry = self.tournament_view.askRetryNewTournament()
                if retry:
                    return self.createNewTournament()
                else:
                    return self.startApp()
        except (ValueError):
            logging.error("Can not create tournament!")
            retry = self.tournament_view.askRetryNewTournament()
            if retry:
                return self.createNewTournament()
            else:
                return self.startApp()

    def addPlayersToTournament(self):
        players_list = Player.getAllPlayers(self)
        self.player_view.displayAllPlayers(players_list)
        players = self.tournament_view.addPlayers()
        Tournament.addPlayers(self, players)
        return self.showCurrentTournaments()

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
        return self.playersMenuChoice()

    def playersMenuChoice(self):
        choice = self.base_view.askUserChoice()
        if choice:
            if choice == "1":
                return self.choosePlayer()
            if choice == "2":
                return self.startApp()
            else:
                return self.playersMenuChoice()
        else:
            return self.playersMenuChoice()

    def playerMenuChoice(self, id):
        player_id = id
        choice = self.base_view.askUserChoice()
        if choice:
            if choice == "1":
                return self.modifyPlayerRanking(player_id)
            if choice == "2":
                return self.startApp()
            else:
                return self.playerMenuChoice()
        else:
            return self.playerMenuChoice()

    def modifyPlayerRanking(self, id):
        id = id
        ranking = self.player_view.askNewRanking()
        Player.modifyRanking(self, id, ranking)
        player = Player.getPlayerById(self, id)
        self.player_view.displayPlayer(player)
        return self.playerMenuChoice(id)

    def sortPlayersByRating(self):
        """sort players by rating"""
        players = Player.getAllPlayers(self)
        players_sorted = sorted(players, key=lambda player: player["rating"], reverse=True)
        self.player_view.displaySortedByRating(players_sorted)
        return self.playersMenuChoice()

    def showCurrentTournaments(self):
        opened_tournament = Tournament.getAllOpenedTournaments(self)
        self.tournament_view.displayTournamentLogs(opened_tournament)
        return self.tournamentsMenuChoice()

    def tournamentsMenuChoice(self):
        choice = self.base_view.askUserChoice()
        if choice:
            if choice == "1":
                return self.chooseTournament()
            if choice == "2":
                return self.startApp()
            else:
                return self.tournamentsMenuChoice()
        else:
            return self.tournamentsMenuChoice()

    def chooseTournament(self):
        choice = self.base_view.askTournamentId()
        if choice:
            tournament = Tournament.getTournamentById(self, choice)
            players = []
            for player in tournament["players"]:
                players.append(Player.getPlayerById(self, player))
            players_sorted = sorted(players, key=lambda player: player["first_name"])
            self.tournament_view.displayTournament(tournament, players_sorted)
            return self.tournamentMenuChoice(choice)

    def tournamentMenuChoice(self, id):
        tournament_id = id
        logging.info(f"Tournament ID: {tournament_id}")
        choice = self.base_view.askUserChoice()
        if choice:
            if choice == "1":
                logging.info(f"User choice: {choice}")
                return self.startTournament(tournament_id)
            if choice == "2":
                logging.info(f"User choice: {choice}")
                return self.startApp()
            else:
                return self.tournamentMenuChoice()
        else:
            return self.tournamentMenuChoice()

    def startTournament(self, id):
        tournament_id = id
        logging.info(f"Tournament ID: {tournament_id}")
        tournament = Tournament.getTournamentById(self, tournament_id)
        games = tournament["games"]
        if games:
            logging.info(f"Tournament games: {games}")
            return self.computeNextRound(tournament_id)
        else:
            logging.info(f"Tournament games: {games}")
            return self.computeFirstRound(tournament_id)

    def computeFirstRound(self, id):
        tournament_id = id
        logging.info(f"Tournament ID: {tournament_id}")
        tournament = Tournament.getTournamentById(self, tournament_id)
        players = []
        for player in tournament["players"]:
            logging.info(f"Player: {player}")
            players.append(Player.getPlayerById(self, player))
        first_round = Round()
        paired_players = first_round.pairPlayers(players, True)
        return self.tournament_view.displayFirstRound(paired_players)

    def computeNextRound(self, id):
        pass

    def generateDummyData(self):
        Player.dummyData(self)
        return self.showAllPlayers()

    def deleteAllTournaments(self):
        Tournament.delTournaments(self)
        return self.showTournamentLogs()
