"""Round Model"""
import logging

from models.database import Database
from models.game import Game


class Round:
    def __init__(self) -> None:
        self.db = Database()
        self.game = Game()

    def pairPlayers(self, players, tournament_id, round: int = 1, first: bool = False):
        """Pair players with swiss rules

        Args:
            players (list): players data
            round (int, optional): round id. Defaults to 1.
            first (bool, optional): if it's first round. Defaults to False.

        Returns:
            list: list of players data sorted
        """
        first = first
        current_round = round
        players = players
        tournament_id = tournament_id
        logging.info(f"pairPlayers init: {players}")
        if first:
            logging.info(f"pairPlayers FIRST players_rating_list: {players}")
            logging.info(f"pairPlayers first: {first}")
            players_sorted = sorted(players, key=lambda player: player["rating"], reverse=True)
            players_id = []
            for player in players_sorted:
                players_id.append(player["id"])
            player_up_id, player_down_id = self.splitPlayers(players_id)
            logging.info(f"player_up_id: {player_up_id} len = {len(player_up_id)}")
            logging.info(f"player_down_id: {player_down_id} len = {len(player_down_id)}")
            for i in range(4):
                logging.info(
                    f"splitPlayers: player_up = {player_up_id[i]}, versus = {player_down_id[i]}, tournament = {int(tournament_id)}"
                )
                self.registerPlayerPair(player_up_id[i], player_down_id[i], int(tournament_id))
                logging.info(
                    f"splitPlayers: player_down = {player_down_id[i]}, versus = {player_up_id[i]}, tournament = {int(tournament_id)}"
                )
                self.registerPlayerPair(player_down_id[i], player_up_id[i], int(tournament_id))
            player_up, player_down = self.splitPlayers(players_sorted)
            paired_players_id = tuple(zip(player_up_id, player_down_id))
            paired_players = tuple(zip(player_up, player_down))
            games = self.game.registerGame(paired_players_id, first=True)
            logging.info(f"pairPlayers FIRST games list: {games}")
            round_number = self.db.insertRound(games, f"Round {current_round}")
            logging.info(f"pairPlayers FIRST round number: {round_number}")
            return paired_players, round
        else:
            next_round = current_round + 1
            logging.info(f"pairPlayers players_score_list: {players}")
            logging.info(f"pairPlayers first: {first}")
            players_sorted = sorted(players, key=lambda player: player["score"], reverse=True)
            players_id = []
            for player in players_sorted:
                players_id.append([player["id"], player["score"]])
            logging.info(f"pairPlayers: {players_id}")
            player_up_id, player_down_id = self.splitPlayers(players_id)
            for i in range(4):
                logging.info(
                    f"splitPlayers: player = {player_up_id[i][0]}, versus = {[player_down_id[i][0]]}, tournament = {int(tournament_id)}"
                )
                paired = self.checkPlayerPair(player_up_id[i][0], [player_down_id[i][0]], int(tournament_id))
                logging.info(f"checkPlayerPair paired = {paired}")
                if paired:
                    initial_pos = i
                    logging.info(f"checkPlayerPair paired loop = {paired}, initial_pos = {initial_pos}")
                    for x in range(3):
                        paired_check = self.checkPlayerPair(
                            player_up_id[i][0], [player_down_id[x + 1][0]], int(tournament_id)
                        )
                        logging.info(f"checkPlayerPair paired_check loop = {paired_check}")
                        if not paired_check:
                            logging.info(f"checkPlayerPair False: {player_up_id[i][0]}, {[player_down_id[x + 1][0]]}")
                            logging.info(f"checkPlayerPair False: {player_down_id[x + 1][0]}, {[player_up_id[i][0]]}")
                            logging.info(
                                f"initial_pos player = {player_down_id[initial_pos]} new pos = {player_down_id[x + 1]}"
                            )
                            logging.info(f"initial list: {player_down_id}")
                            self.swapPlayers(player_down_id, (x + 1), initial_pos)
                            logging.info(f"new list: {player_down_id}")
                            self.updatePlayerPair(player_up_id[i][0], [player_down_id[x + 1][0]], int(tournament_id))
                            self.updatePlayerPair(player_down_id[x + 1][0], [player_up_id[i][0]], int(tournament_id))
                else:
                    self.updatePlayerPair(player_up_id[i][0], [player_down_id[i][0]], int(tournament_id))
                    self.updatePlayerPair(player_down_id[i][0], [player_up_id[i][0]], int(tournament_id))
            player_up, player_down = self.splitPlayers(players_sorted)
            paired_players_id = tuple(zip(player_up_id, player_down_id))
            paired_players = tuple(zip(player_up, player_down))
            games = self.game.registerGame(paired_players_id)
            logging.info(f"pairPlayers games list: {games}")
            round_number = self.db.insertRound(games, f"Round {next_round}")
            logging.info(f"pairPlayers round number: {next_round}")
            return paired_players, round_number

    def registerPlayerPair(self, player_id, player_versus_id, tournament_id):
        player_id = player_id
        player_versus_id = player_versus_id
        tournament_id = tournament_id
        return self.db.insertPlayerPair(player_id, player_versus_id, tournament_id)

    def updatePlayerPair(self, player_id, player_versus_id, tournament_id):
        player_id = player_id
        player_versus_id = player_versus_id
        tournament_id = tournament_id
        return self.db.updatePlayerPair(player_id, player_versus_id, tournament_id)

    def checkPlayerPair(self, player_id, player_versus_id, tournament_id):
        player_id = player_id
        player_versus_id = player_versus_id
        tournament_id = tournament_id
        return self.db.checkPlayerPair(player_id, player_versus_id, tournament_id)

    def swapPlayers(self, players_list, pos1, pos2):
        first_ele = players_list.pop(pos1)
        second_ele = players_list.pop(pos2)

        players_list.insert(pos1, second_ele)
        players_list.insert(pos2, first_ele)
        return players_list

    def getPairedPlayers(self, players, first: bool = False):
        """Get paired players data

        Args:
            players (list): players data
            first (bool, optional): if it's first paired. Defaults to False.

        Returns:
            list: list of players data
        """
        first = first
        players = players
        logging.info(f"getPairedPlayers init: {players}")
        if first:
            logging.info(f"getPairedPlayers FIRST players_rating_list: {players}")
            logging.info(f"getPairedPlayers first: {first}")
            players_sorted = sorted(players, key=lambda player: player["rating"], reverse=True)
            player_up, player_down = self.splitPlayers(players_sorted)
            paired_players = tuple(zip(player_up, player_down))
            return paired_players
        else:
            logging.info(f"getPairedPlayers players_score_list: {players}")
            logging.info(f"getPairedPlayers first: {first}")
            players_sorted = sorted(players, key=lambda player: player["score"], reverse=True)
            player_up, player_down = self.splitPlayers(players_sorted)
            paired_players = tuple(zip(player_up, player_down))
            logging.info(f"getPairedPlayers sorted: {paired_players}")
            return paired_players

    def splitPlayers(self, players):
        """Split player list in half"""
        players = players
        list_len = len(players)
        middle = list_len // 2
        players_up = players[:middle]
        players_down = players[middle:]
        return players_up, players_down

    def endRound(self, round):
        """End round"""
        round_id = round
        return self.db.endRound(round_id)

    def getPlayersFromGames(self, id):
        """Grab players from games"""
        round_id = id
        round = self.db.getRoundById(round_id)
        games = round["games"]
        players = []
        for game in games:
            players.append(Game.getPlayers(self, game))
        players_list = []
        for player in players:
            players_list.append(self.db.getPlayerById(player["player1"]))
            players_list.append(self.db.getPlayerById(player["player2"]))
        return players_list

    def getScoreFromGames(self, round):
        """Grab scores from games"""
        round_id = round
        round = self.db.getRoundById(round_id)
        games = round["games"]
        scores1 = []
        scores2 = []
        for game in games:
            score = self.db.getScores(game)
            scores1.extend((score["player1"], score["player2"]))
            scores2.extend((score["score1"], score["score2"]))
        scores = tuple(zip(scores1, scores2))
        return scores

    def getGamesFromRound(self, round_id):
        """Grab games from round"""
        round_id = round_id
        games = self.db.getGamesFromRound(round_id)
        return games
