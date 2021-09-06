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

    def getPlayers(self, id):
        game_id = id
        players = self.db.getPlayersIdFromGame(game_id)
        return players
