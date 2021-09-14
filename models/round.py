import logging

from models.database import Database
from models.game import Game


class Round:
    def __init__(self) -> None:
        self.db = Database()
        self.game = Game()

    def pairPlayers(self, players, round: int = 1, first: bool = False):
        first = first
        current_round = round
        players = players
        logging.info(f"pairPlayers init: {players}")
        if first:
            logging.info(f"pairPlayers FIRST players_rating_list: {players}")
            logging.info(f"pairPlayers first: {first}")
            players_sorted = sorted(players, key=lambda player: player["rating"], reverse=True)
            players_id = []
            for player in players_sorted:
                players_id.append(player["id"])
            player_up_id, player_down_id = self.splitPlayers(players_id)
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
            player_up, player_down = self.splitPlayers(players_sorted)
            paired_players_id = tuple(zip(player_up_id, player_down_id))
            paired_players = tuple(zip(player_up, player_down))
            games = self.game.registerGame(paired_players_id)
            logging.info(f"pairPlayers games list: {games}")
            round_number = self.db.insertRound(games, f"Round {next_round}")
            logging.info(f"pairPlayers round number: {next_round}")
            return paired_players, round_number

    def getPairedPlayers(self, players, first: bool = False):
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
            return paired_players

    def splitPlayers(self, players):
        players = players
        list_len = len(players)
        middle = list_len // 2
        players_up = players[:middle]
        players_down = players[middle:]
        return players_up, players_down

    def endRound(self, round):
        round_id = round
        return self.db.endRound(round_id)

    def getPlayersFromGames(self, id):
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
        round_id = round_id
        games = self.db.getGamesFromRound(round_id)
        return games
