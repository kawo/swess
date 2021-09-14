"""Main Controller for SWESS"""
import logging
import sys

from models.game import Game
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
        logging.info("Calling displayMainMenu...")
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
            logging.info("Displaying all players...")
            return self.showAllPlayers()
        if choice == "2":
            logging.info("Displaying ranking...")
            return self.sortPlayersByRating()
        if choice == "3":
            logging.info("Displaying tournaments logs...")
            return self.showTournamentLogs()
        if choice == "4":
            logging.info("Displaying current opened tournaments...")
            return self.showCurrentTournaments()
        if choice == "5":
            logging.info("Creating new player...")
            return self.addPlayer()
        if choice == "6":
            logging.info("Creating new tournament...")
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

    def tournamentMenuChoice(self, tournament):
        tournament_id = tournament
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
                return self.tournamentMenuChoice(tournament_id)
        else:
            return self.tournamentMenuChoice(tournament_id)

    def startTournament(self, id):
        tournament_id = id
        logging.info(f"Tournament ID: {tournament_id}")
        tournament = Tournament.getTournamentById(self, tournament_id)
        rounds = tournament["rounds"]
        rounds_len = len(rounds)
        if rounds_len != 0:
            if rounds_len == 1:
                round_ended = Tournament.checkRoundEndTime(self, tournament_id)
                logging.info(f"startTournament round_ended: {round_ended}")
                if not round_ended:
                    logging.info("First round not ended, resuming...")
                    return self.computeFirstRound(tournament_id)
            logging.info(f"Tournament current round: {rounds_len}")
            return self.continueTournament(rounds_len, tournament_id)
        else:
            logging.info("First Tournament Round")
            return self.computeFirstRound(tournament_id)

    def continueTournament(self, round, tournament_id):
        tournament_id = tournament_id
        current_round = round
        check = Tournament.checkRoundEndTime(self, tournament_id)
        if check:
            return self.computeNextRound(tournament_id, current_round)
        else:
            games = Round.getGamesFromRound(self, current_round)
            logging.info(f"continueTournament games list: {games}")
            players = Game.getPlayersFromGames(self, games)
            logging.info(f"Players list from Round {current_round}: {players}")
            paired = Round()
            paired_players = paired.getPairedPlayers(players)
            logging.info(f"continueTournament paired_players: {paired_players}")
            self.tournament_view.displayRound(current_round, players, games)
            return self.roundMenuChoice(current_round, tournament_id)

    def computeFirstRound(self, id):
        tournament_id = id
        logging.info(f"Tournament ID: {tournament_id}")
        tournament = Tournament.getTournamentById(self, tournament_id)
        players = []
        for player in tournament["players"]:
            logging.info(f"Player: {player}")
            players.append(Player.getPlayerById(self, player))
        rounds = tournament["rounds"]
        rounds_len = len(rounds)
        if rounds_len == 0:
            first_round = Round()
            paired_players, round = first_round.pairPlayers(players, first=True)
            logging.info(f"computeFirstRound players: {paired_players}")
            logging.info(f"computeFirstRound ID: {round}")
            logging.info("Registering new round...")
            Tournament.registerRoundToTournament(self, round, tournament_id)
        else:
            round = rounds_len
            round_player = Round()
            paired_players = round_player.getPairedPlayers(players, first=True)
        self.tournament_view.displayFirstRound(paired_players)
        return self.roundMenuChoice(round, tournament_id)

    def roundMenuChoice(self, round, tournament_id):
        round_id = round
        tournament_id = tournament_id
        logging.info(f"Round ID: {round_id}")
        choice = self.base_view.askUserChoice()
        if choice:
            if choice == "1":
                logging.info(f"User choice: {choice}")
                return self.enterResults(round_id, tournament_id)
            if choice == "2":
                logging.info("Ending round...")
                Round.endRound(self, round_id)
                return self.computeNextRound(tournament_id, round_id)
            if choice == "3":
                logging.info(f"User choice: {choice}")
                return self.startApp()
            else:
                return self.roundMenuChoice(round_id, tournament_id)
        else:
            return self.roundMenuChoice(round_id, tournament_id)

    def enterResults(self, round, tournament_id):
        round_id = round
        tournament_id = tournament_id
        game_id = self.tournament_view.askUserGame()
        if game_id:
            logging.info(f"enterResults game_id: {game_id}")
            players = Game.getPlayersFromGames(self, game_id)
            self.tournament_view.showGame(players, game_id)
            player_id = self.base_view.askUser("Enter Player ID: ")
            score = self.base_view.askUser("Enter score (1, 0.5, 0): ")
            add_score = Game()
            add_score.addScore(game_id, player_id, score)
            if round_id == 1:
                round_ended = Tournament.checkRoundEndTime(self, tournament_id)
                if not round_ended:
                    logging.info("enterResults: computeFirstRound")
                    return self.computeFirstRound(tournament_id)
                else:
                    logging.info("enterResults: continueTournament")
                    return self.continueTournament(round_id, tournament_id)
            logging.info("enterResults: continueTournament")
            return self.continueTournament(round_id, tournament_id)
        else:
            return self.enterResults(round_id)

    def showGame(self, game):
        game_id = game
        result = Game.getGame(self, game_id)
        return result

    def computeNextRound(self, tournament_id, round_id):
        tournament_id = tournament_id
        round_id = round_id
        games = Round.getGamesFromRound(self, round_id)
        logging.info(f"computeNextRound games list: {games}")
        players = Game.getPlayersFromGames(self, games)
        logging.info(f"Players list from Round {round_id}: {players}")
        round = Round()
        paired_players, next_round = round.pairPlayers(players, round=round_id)
        logging.info(f"computeNextRound: {paired_players}")
        logging.info(f"computeNextRound ID: {next_round}")
        Tournament.registerRoundToTournament(self, next_round, tournament_id)
        paired_players = Game.getPlayersFromGames(self, games)
        logging.info(f"displayRound: Round {round_id}, {paired_players}")
        self.tournament_view.displayRound(round_id, paired_players, games)
        return self.roundMenuChoice(next_round, tournament_id)

    def generateDummyData(self):
        Player.dummyData(self)
        return self.showAllPlayers()

    def deleteAllTournaments(self):
        Tournament.delTournaments(self)
        return self.showTournamentLogs()
