import logging

from models.database import Database


class Game:
    def __init__(self) -> None:
        self.db = Database()

    def registerGame(self, players):
        players = players
        games_id = []
        for player in players:
            games_id.append(self.db.insertPairedPlayer(player))
        return games_id

    def getPlayersFromGame(self, id):
        game_id = id
        players = Game.getGame(self, game_id)
        logging.info(f"players = {players}")
        players_list = []
        players_list.append(self.db.getPlayerById(players["player1"]))
        players_list.append(self.db.getPlayerById(players["player2"]))
        players_list[0].update([("score", players["score1"])])
        players_list[1].update([("score", players["score2"])])
        logging.info(f"players_list = {players_list}")
        return players_list

    def getPlayers(self, id):
        game_id = id
        players = self.db.getPlayersIdFromGame(game_id)
        return players

    def getGame(self, game):
        game_id = game
        result = self.db.getGame(game_id)
        return result

    def addScore(self, game, player, score):
        game_id = game
        player_id = player
        score = score
        result = self.db.modifyScore(game_id, player_id, score)
        return result
