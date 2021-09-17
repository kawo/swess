"""Database Model"""
import logging
from datetime import datetime

import tinydb
from rich.console import Console
from tinydb.operations import add
from tinydb.queries import Query, where


class Database:
    def __init__(self) -> None:
        self.db = tinydb.TinyDB("db.json", ensure_ascii=False)
        self.players_table = self.db.table("players")
        self.tournament_table = self.db.table("tournaments")
        self.rounds_table = self.db.table("rounds")
        self.games_table = self.db.table("games")
        self.paired_players = self.db.table("paired")
        self.console = Console()

    def serializePlayer(self, value) -> dict:
        """serialize player for database insert

        Args:
            value (Player): player object.

        Returns:
            dict: return a player in dict format.
        """
        logging.info("Serializing player...")
        self.player = value
        serialized_player = {
            "first_name": self.player.first_name,
            "last_name": self.player.last_name,
            "gender": self.player.gender,
            "birthday": self.player.birthday,
            "rating": self.player.rating,
        }
        return serialized_player

    def checkPlayerExists(self, value: dict) -> bool:
        """check if player exists before adding to db

        Args:
            value (dict): value to check.

        Returns:
            bool: return True if entry exist.
        """
        logging.info("Checking if player already exist in database...")
        check = False
        last_name = value["last_name"]
        first_name = value["first_name"]
        if last_name != "" and first_name != "":
            if self.players_table.search(where("last_name") == last_name) and self.players_table.search(
                where("first_name") == first_name
            ):
                self.console.print(f"[bold red]Player {first_name} {last_name} already exist![/bold red]")
                logging.warning("Player already exist!")
                check = True
            else:
                logging.info("Player does not exist")
                check = False
        else:
            check = False
        return check

    def insertPlayer(self, value, serialize: bool) -> bool:
        """insert a player to the database

        Args:
            value (Player): Player object to insert.
        """
        insert = False
        serialize = serialize
        logging.info(f"serialize = {serialize}")
        if serialize:
            logging.info(f"serialize = {serialize}")
            self.value = self.serializePlayer(value)
        else:
            self.value = value
        if self.checkPlayerExists(self.value) is False:
            if self.players_table.insert(self.value):
                logging.info("Player inserted in database!")
                insert = True
            else:
                logging.warning("Player not inserted in database!")
                insert = False
        return insert

    def insertPlayerPair(self, player_id, player_versus_id, tournament_id):
        player_id = player_id
        player_versus_id = [player_versus_id]
        tournament_id = tournament_id
        result = {"player": player_id, "versus": player_versus_id, "tournament": tournament_id}
        logging.info(f"insertPlayerPair result: {result}")
        return self.paired_players.insert(result)

    def updatePlayerPair(self, player_id, player_versus_id, tournament_id):
        player_id = player_id
        player_versus_id = player_versus_id
        tournament_id = tournament_id
        logging.info(
            f"updatePlayerPair: player = {player_id}, tournament = {tournament_id}, versus = {player_versus_id}"
        )
        return self.paired_players.update(
            add("versus", player_versus_id), ((where("player") == player_id) & (where("tournament") == tournament_id))
        )

    def checkPlayerPair(self, player_id, player_versus_id, tournament_id):
        player_id = player_id
        player_versus_id = player_versus_id
        tournament_id = tournament_id
        logging.info(f"checkPlayerPair: player = {player_id}, versus = {player_versus_id}")
        Paired = Query()
        result = self.paired_players.contains(
            (Paired.player == player_id) & (Paired.tournament == tournament_id) & (Paired.versus.any(player_versus_id))
        )
        logging.info(f"checkPlayerPair result: {result}")
        return result

    def getAll(self, value: str):
        """Get all data from specified table"""
        table = value
        if table == "players":
            logging.info("Getting all players from database...")
            result = self.players_table.all()
            return result
        if table == "tournaments":
            logging.info("Getting all tournaments from database...")
            result = self.tournament_table.all()
            return result
        else:
            logging.error(f"{table} table does not exists!")
            return None

    def getOpenedTournaments(self):
        """Get only tournament with no end date"""
        opened_tournaments = []
        tournaments = self.tournament_table.all()
        for tournament in tournaments:
            end_date = tournament["end_date"]
            if end_date is None:
                opened_tournaments.append(tournament)
        return opened_tournaments

    def serializeTournament(self, value) -> dict:
        """Serialize tournament for database insert

        Args:
            value (Tournament): tournament object.

        Returns:
            dict: return a tournament in dict format.
        """
        logging.info("Serializing tournament...")
        self.tournament = value
        serialized_tournament = {
            "name": self.tournament.name,
            "location": self.tournament.location,
            "rounds_number": self.tournament.rounds_number,
            "time_type": self.tournament.time_type,
            "description": self.tournament.description,
            "date": self.tournament.date,
            "rounds": self.tournament.rounds,
            "end_date": self.tournament.end_date,
            "players": self.tournament.players,
        }
        return serialized_tournament

    def registerTournament(self, value: object) -> bool:
        """Register new tournament to database

        Args:
            value (Tournament): Tournament object to insert.
        """
        insert = False
        self.value = self.serializeTournament(value)
        if self.tournament_table.insert(self.value):
            logging.info("Tournament registered in database!")
            insert = True
        else:
            logging.warning("Tournament not registered in database!")
            insert = False
        logging.info(f"Insert: {insert}")
        return insert

    def insertRound(self, games, name, date_ended: str = None):
        """Insert a round

        Args:
            games (list): list of games
            name (str): round name
            date_ended (str, optional): date when round is ended. Defaults to None.

        Returns:
            bool: True if successfull
        """
        games_list = games
        round_name = name
        date_ended = date_ended
        now = datetime.now()
        date_now = now.strftime("%d/%m/%Y - %H:%M:%S")
        round = {"name": round_name, "games": games_list, "date_started": date_now, "date_ended": date_ended}
        return self.rounds_table.insert(round)

    def endRound(self, round):
        """End round"""
        round_id = round
        now = datetime.now()
        date_now = now.strftime("%d/%m/%Y - %H:%M:%S")
        return self.rounds_table.update({"date_ended": date_now}, doc_ids=[round_id])

    def endTournament(self, tournament_id):
        """End tournament"""
        tournament_id = int(tournament_id)
        now = datetime.now()
        date_now = now.strftime("%d/%m/%Y - %H:%M:%S")
        logging.info(f"End Date: {date_now}, Tournament ID: {tournament_id}")
        return self.tournament_table.update({"end_date": date_now}, doc_ids=[tournament_id])

    def insertPairedPlayer(self, players, first: bool = False):
        """Insert paired players

        Args:
            players (tuple): paired players
            first (bool, optional): [description]. Defaults to False.

        Returns:
            int: return new game id
        """
        paired_players = players
        first = first
        if first:
            game_id = self.games_table.insert(
                {"player1": paired_players[0], "score1": 0.0, "player2": paired_players[1], "score2": 0.0}
            )
            logging.info(f"insertPairedPlayer: {game_id}")
        else:
            game_id = self.games_table.insert(
                {
                    "player1": paired_players[0][0],
                    "score1": paired_players[0][1],
                    "player2": paired_players[1][0],
                    "score2": paired_players[1][1],
                }
            )
            logging.info(f"insertPairedPlayer: {game_id}")
        return game_id

    def addPlayers(self, value) -> bool:
        """Add player to tournament"""
        players = value
        players_exists = self.checkPlayerID(players)
        if players_exists:
            last_tournament = self.tournament_table.get(doc_id=len(self.db))
            self.tournament_table.update({"players": players}, doc_ids=last_tournament)
            return players_exists
        else:
            return players_exists

    def checkPlayerID(self, value) -> bool:
        """Check if player ID exists"""
        players = value
        player_exists = True
        for player in players:
            logging.info(f"Checking Player ID: {player}")
            check_id = self.players_table.contains(doc_id=int(player))
            logging.info(f"{check_id}")
            if check_id:
                logging.info(f"Player ID {player} exists!")
            else:
                player_exists = False
                logging.error(f"Player ID {player} does not exists!")
        return player_exists

    def checkRoundEndTime(self, tournament_id) -> bool:
        """Check if round is ended

        Args:
            tournament_id (list): tournament data

        Returns:
            bool: True if round is ended
        """
        tournament_id = tournament_id
        tournament = self.getTournamentById(tournament_id)
        check = False
        last_round_id = len(tournament["rounds"])
        logging.info(f"last_round_id = {last_round_id}")
        round = self.rounds_table.get(doc_id=last_round_id)
        date_ended = round["date_ended"]  # type: ignore
        logging.info(f"Round date_ended: {date_ended}")
        if date_ended:
            check = True
        return check

    def getPlayerById(self, value):
        """Grab player by ID"""
        id = int(value)
        player = self.players_table.get(doc_id=id)
        player.update({"id": id})
        return player

    def getRoundById(self, id):
        """Grab round by ID"""
        round_id = int(id)
        round = self.rounds_table.get(doc_id=round_id)
        return round

    def getPlayersIdFromGame(self, id):
        """Grab player from a game"""
        game_id = int(id)
        players = self.games_table.get(doc_id=game_id)
        return players

    def getScores(self, game):
        """Grab score from a game"""
        game = game
        result = self.games_table.get(doc_id=game)
        logging.info(f"Scores: {result}")
        return result

    def getTournamentById(self, value):
        """Grab tournament by ID"""
        id = int(value)
        tournament = self.tournament_table.get(doc_id=id)
        return tournament

    def getGame(self, game):
        """Get game by ID"""
        game_id = int(game)
        game = self.games_table.get(doc_id=game_id)
        return game

    def getGamesFromRound(self, round_id):
        """Grab games list from round"""
        round_id = int(round_id)
        round = self.rounds_table.get(doc_id=round_id)
        games = []
        for game in round["games"]:
            games.append(game)
        logging.info(f"Games list: {games}")
        return games

    def registerRound(self, round, id):
        """Register round in tournament"""
        round = [round]
        tournament_id = int(id)
        logging.info(f"registerRound numbet {round} to {tournament_id}")
        result = self.tournament_table.update(add("rounds", round), doc_ids=[tournament_id])
        return result

    def modifyRanking(self, id, ranking):
        """Modify ranking of player"""
        id = int(id)
        ranking = int(ranking)
        return self.players_table.update({"rating": ranking}, doc_ids=[id])

    def modifyScore(self, game, player, score):
        """Modify score of player"""
        game_id = int(game)
        player_id = int(player)
        score = float(score)
        logging.info(f"modifyScore: {game_id}, {player_id}, {score}")
        result = self.games_table.get(doc_id=game_id)
        if result["player1"] == player_id:
            return self.games_table.update({"score1": score}, doc_ids=[game_id])
        if result["player2"] == player_id:
            return self.games_table.update({"score2": score}, doc_ids=[game_id])
