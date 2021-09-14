import logging

from models.database import Database


class Game:
    def __init__(self) -> None:
        self.db = Database()

    def registerGame(self, players, first: bool = False):
        first = first
        players = players
        games_id = []
        for player in players:
            games_id.append(self.db.insertPairedPlayer(player, first=first))
        return games_id

    def getPlayersFromGames(self, games_list):
        games_list = games_list
        logging.info(f"getPlayersFromGames games_list = {games_list}")
        players_list = []
        i = 0
        for game in games_list:
            logging.info(f"getPlayersFromGames game = {game}")
            logging.info(f"i = {i}")
            players = Game.getGame(self, game)
            logging.info(f"getPlayersFromGames players = {players}")
            players_list.append(self.db.getPlayerById(players["player1"]))
            logging.info(f"getPlayersFromGames player1 = {players['player1']}")
            players_list.append(self.db.getPlayerById(players["player2"]))
            logging.info(f"getPlayersFromGames player2 = {players['player2']}")
            players_list[i].update([("score", players["score1"])])
            logging.info(f"getPlayersFromGames score1 = {players['score1']}")
            players_list[i + 1].update([("score", players["score2"])])
            logging.info(f"getPlayersFromGames score2 = {players['score2']}")
            i = i + 2
        logging.info(f"getPlayersFromGames players_list = {players_list}")
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
