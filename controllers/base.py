from views.base import BaseView
from rich.console import Console


class BaseController:
    def __init__(self) -> None:
        self.console = Console()
        self.view = BaseView()

    def showMainMenu(self):
        """tell the view to show the main menu"""
        self.view.displayMainMenu()
        choice = self.console.input("Entrez le numéro correspondant à votre choix : ")
        self.mainMenuChoice(choice)

    def mainMenuChoice(self, value: str) -> None:
        """user choice from main menu

        Args:
            value (str): user input for menu item.

        Returns:
            approriate view for the choice
        """
        self.choice = value
        if self.choice == "1":
            self.view.displayAllPlayers()
        if self.choice == "4":
            self.view.displayAddPlayer()
        return None
