from models.database import Database


class Game:
    def __init__(self) -> None:
        self.db = Database()

    def registerGame(self, players):
        players = players
        games_id = []
        for player in players:
            games_id.append(self.db.insertPairedPlayer({player[0]: 0, player[1]: 0}))
        return games_id
