"""Game Model"""
import logging

from models.database import Database


class Game:
    def __init__(self) -> None:
        self.db = Database()

    def registerGame(self, players, first: bool = False):
        """Register new game

        Args:
            players (tuple): players pairs
            first (bool, optional): if it's first game. Defaults to False.

        Returns:
            int: return game id
        """
        first = first
        players = players
        games_id = []
        for player in players:
            games_id.append(self.db.insertPairedPlayer(player, first=first))
        return games_id

    def getPlayersFromGames(self, games_list):
        """Get players from games"""
        games_list = games_list
        logging.info(f"getPlayersFromGames games_list = {games_list}")
        players_list = []
        i = 0
        game_len = len(games_list)
        logging.info(f"getPlayersFromGames len: {game_len}")
        if game_len == 2:
            games_list = games_list[0] + games_list[1]
            logging.info(f"getPlayersFromGame game = {games_list}")
            logging.info(f"i = {i}")
            players = Game.getGame(self, games_list)
            logging.info(f"getPlayersFromGame players = {players}")
            players_list.append(self.db.getPlayerById(players["player1"]))
            logging.info(f"getPlayersFromGame player1 = {players['player1']}")
            players_list.append(self.db.getPlayerById(players["player2"]))
            logging.info(f"getPlayersFromGame player2 = {players['player2']}")
            players_list[i].update([("score", players["score1"])])
            logging.info(f"getPlayersFromGame score1 = {players['score1']}")
            players_list[i + 1].update([("score", players["score2"])])
            logging.info(f"getPlayersFromGame score2 = {players['score2']}")
        else:
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
        """Get player data from game"""
        game_id = id
        players = self.db.getPlayersIdFromGame(game_id)
        return players

    def getGame(self, game):
        """Get game"""
        game_id = game
        result = self.db.getGame(game_id)
        return result

    def addScore(self, game, player_id, score):
        """Add/Modify score"""
        game_id = game
        player_id = int(player_id)
        score = float(score)
        players = self.getGame(game_id)
        logging.info(f"addScore players: {players}")
        if players["player1"] == player_id:
            score = score + float(players["score1"])
            logging.info(f"addScore Player {players['player1']} total score: {score}")
        if players["player2"] == player_id:
            score = score + float(players["score2"])
            logging.info(f"addScore Player {players['player1']} total score: {score}")
        result = self.db.modifyScore(game_id, player_id, score)
        return result
