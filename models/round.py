class Round:

    def __init__(self) -> None:
        pass

    def pairPlayers(self, players, first: bool = False):
        first = first
        players = players
        if first:
            player_up, player_down = self.splitPlayers(players)
            paired_players = tuple(zip(player_up, player_down))
            return paired_players

    def splitPlayers(self, players):
        players = players
        list_len = len(players)
        middle = list_len // 2
        players_up = players[:middle]
        players_down = players[middle:]
        return players_up, players_down
