import logging
from datetime import datetime

import tinydb
from rich.console import Console
from tinydb.queries import where


class Database:
    def __init__(self) -> None:
        self.db = tinydb.TinyDB("db.json", ensure_ascii=False)
        self.players_table = self.db.table("players")
        self.tournament_table = self.db.table("tournaments")
        self.rounds_table = self.db.table("rounds")
        self.games_table = self.db.table("games")
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

    def getAll(self, value: str):
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
        games_list = games
        round_name = name
        date_ended = date_ended
        now = datetime.now()
        date_now = now.strftime("%d/%m/%Y - %H:%M:%S")
        round = {"name": round_name, "games": games_list, "date_started": date_now, "date_ended": date_ended}
        return self.rounds_table.insert(round)

    def insertPairedPlayer(self, players):
        paired_players = players
        game_id = self.games_table.insert(paired_players)
        return game_id

    def addPlayers(self, value) -> bool:
        players = value
        players_exists = self.checkPlayerID(players)
        if players_exists:
            last_tournament = self.tournament_table.get(doc_id=len(self.db))
            self.tournament_table.update({"players": players}, doc_ids=last_tournament)
            return players_exists
        else:
            return players_exists

    def checkPlayerID(self, value) -> bool:
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

    def checkRoundEndTime(self, tournament) -> bool:
        tournament = tournament
        check = False
        last_round_id = len(tournament["rounds"])
        logging.info(f"last_round_id = {last_round_id}")
        round = self.rounds_table.get(doc_id=last_round_id)
        logging.info(round)
        date_ended = round["date_ended"]
        logging.info(date_ended)
        if date_ended:
            check = True
        return check

    def getPlayerById(self, value):
        id = int(value)
        player = self.players_table.get(doc_id=id)
        return player

    def getRoundById(self, id):
        round_id = int(id)
        round = self.rounds_table.get(doc_id=round_id)
        return round

    def getPlayersIdFromGame(self, id):
        game_id = int(id)
        players = self.games_table.get(doc_id=game_id)
        players_list = []
        for player in players:
            players_list.append(player)
        return players_list

    def getTournamentById(self, value):
        id = int(value)
        tournament = self.tournament_table.get(doc_id=id)
        return tournament

    def registerRound(self, round, id):
        round = [round]
        tournament_id = int(id)
        logging.info(f"{round} {tournament_id}")
        result = self.tournament_table.update({"rounds": round}, doc_ids=[tournament_id])
        return result

    def modifyRanking(self, id, ranking):
        id = int(id)
        ranking = int(ranking)
        return self.players_table.update({"rating": ranking}, doc_ids=[id])
