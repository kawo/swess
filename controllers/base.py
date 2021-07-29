"""Main Controller for SWESS"""
import logging
import sys

import views.console
from models.player import Player


class Controller:
    def __init__(self) -> None:
        self.base_view = views.console.base.BaseView()
        self.player_view = views.console.player.PlayerView()

    def startApp(self):
        """Show Main Menu

        Returns:
            Display Main Menu
        """
        logging.info("Calling view.displayMainMenu")
        choice = self.base_view.displayMainMenu()
        self.getMainMenuChoice(choice)

    def getMainMenuChoice(self, choice: str):
        """Get user choice

        Args:
            choice (str): User choice from Main Menu.
        """
        choice = choice
        if choice == "":
            self.base_view.printToUser("[bold red]You must type a number![/bold red]\n")
            logging.warning("User input is empty")
            return self.startApp()
        if choice == "1":
            logging.info("Calling view.displayAllPlayers()")
            return self.showAllPlayers()
        if choice == "3":
            logging.info("Calling controller player.sortPlayersByRating()")
            return self.sortPlayersByRating()
        if choice == "4":
            logging.info("Calling controller player.addPlayer()")
            return self.addPlayer()
        if choice == "6":
            self.base_view.printToUser("Byyye!")
            logging.info("Program terminated by the user")
            return sys.exit()
        else:
            logging.warning("User input is wrong")
            logging.warning("Returning to Main Menu...")
            return self.startApp()

    def returnToMainMenu(self):
        choice = self.base_view.askReturnToMainMenu()
        if choice:
            self.startApp()

    def addPlayer(self):
        player = self.player_view.displayAddPlayer()
        first_name = player["first_name"]
        last_name = player["last_name"]
        birthday = player["birthday"]
        gender = player["gender"]
        rating = player["rating"]
        try:
            if rating:
                new_player = Player(first_name, last_name, birthday, gender, int(rating))
            else:
                new_player = Player(first_name, last_name, birthday, gender)
            logging.info("Player successfully created!")
            logging.info("Trying to add player to database...")
            if new_player.addToDb(new_player):
                logging.info("Player successfully inserted in database!")
                if rating:
                    self.base_view.printToUser(
                        f"[bold green]Player: {first_name} {last_name}, {gender} gender, born on {birthday} with a ranking of {rating} added in database![/bold green]"
                    )
                else:
                    self.base_view.printToUser(
                        f"[bold green]Player: {first_name} {last_name}, {gender} gender, born on {birthday} with a ranking of 0 added in database![/bold green]"
                    )
            else:
                logging.error("Can not insert player in database !")
                retry = self.player_view.askRetryAddPlayer()
                if retry:
                    return self.addPlayer()
                else:
                    return self.startApp()
        except (TypeError, ValueError):
            logging.error("Can not create player!")
            retry = self.player_view.askRetryAddPlayer()
            if retry:
                return self.addPlayer()
            else:
                return self.startApp()

    def showAllPlayers(self):
        """ask model for all the players"""
        players = Player.getAllPlayers(self)
        self.player_view.displayAllPlayers(players)
        return self.returnToMainMenu()

    def sortPlayersByRating(self):
        """sort players by rating"""
        players = Player.getAllPlayers(self)
        players_sorted = sorted(players, key=lambda player: player["rating"], reverse=True)
        self.player_view.displaySortedByRating(players_sorted)
        return self.returnToMainMenu()
