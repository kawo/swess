"""SWESS Chess Tournament Manager"""
import logging
import signal
import sys
from datetime import date

import controllers
from views.console.base import BaseView

today = date.today().strftime("%d-%m-%Y")

logging.basicConfig(
    filename=f"logs/{today}.log",
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    encoding="utf-8",
    level=logging.DEBUG,
)  # type: ignore
# mypy reportly false attr 'encoding' for logging


def manualExit(signal, frame):
    """Gracefull exit when user press CTRL+C

    Args:
        signal: signal number
        frame: current stack frame

    Returns:
        exit program with 0 (no error)
    """
    view = BaseView()
    view.printToUser("\n[bold red]You ended the program with CTRL+C![/bold red]")
    logging.info("Program ended by CTRL+C")
    return sys.exit(0)


def main():
    """main loop"""
    logging.info("App started...")
    swess = controllers.base.Controller()
    swess.startApp()
    logging.info("App finished.")


if __name__ == "__main__":
    signal.signal(signal.SIGINT, manualExit)
    main()
