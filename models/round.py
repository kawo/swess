import logging

from models.database import Database
from models.game import Game


class Round:
    def __init__(self) -> None:
        self.db = Database()
        self.game = Game()

    def pairPlayers(self, players, first: bool = False):
        first = first
        players = players
        if first:
            players_sorted = sorted(players, key=lambda player: player["rating"], reverse=True)
            players_id = []
            for player in players_sorted:
                players_id.append(player["id"])
            player_up_id, player_down_id = self.splitPlayers(players_id)
            player_up, player_down = self.splitPlayers(players_sorted)
            paired_players_id = tuple(zip(player_up_id, player_down_id))
            paired_players = tuple(zip(player_up, player_down))
            games = self.game.registerGame(paired_players_id)
            logging.info(games)
            round = self.db.insertRound(games, "Round 1")
            logging.info(round)
            return paired_players, round

    def splitPlayers(self, players):
        players = players
        list_len = len(players)
        middle = list_len // 2
        players_up = players[:middle]
        players_down = players[middle:]
        return players_up, players_down
