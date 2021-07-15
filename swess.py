import logging
from datetime import date

from controllers.base import Controller

today = date.today().strftime("%d-%m-%Y")

logging.basicConfig(
    filename=f"logs/{today}.log",
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    encoding="utf-8",
    level=logging.DEBUG,
)  # type: ignore
# mypy reportly false attr 'encoding' for logging


def main():
    """main loop"""
    logging.info("App started...")
    swess = Controller()
    swess.startApp()
    logging.info("App finished.")


if __name__ == "__main__":
    main()
