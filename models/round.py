class Round:
    def __init__(self) -> None:
        pass

    def pairPlayers(self, players, first: bool = False):
        first = first
        players = players
        if first:
            players_sorted = sorted(players, key=lambda player: player["rating"], reverse=True)
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
