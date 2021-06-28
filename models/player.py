from models.validator import Choice, Date, FloatPositive, String


class Player:
    """A player of chess tournament

    Args:
        last_name (str): last name.
        first_name (str): first name.
        birthday (str): date of birth.
        sex (str): sex (M or F).
        rating (int, optional): rating of player. Defaults to 0.0.
    """

    last_name = String(minsize=3, maxsize=30, name="Nom")
    first_name = String(minsize=3, maxsize=30, name="Prénom")
    sex = Choice("Sexe", "M", "F")
    birthday = Date("Anniversaire", "%d/%m/%Y")
    rating = FloatPositive("Classement")

    def __init__(self, last_name: str, first_name: str, birthday: str, sex: str, rating=0.0):
        self.last_name = last_name
        self.first_name = first_name
        self.sex = sex
        self.rating = rating
        self.birthday = birthday

    def __str__(self) -> str:
        return f"- Joueur -\nNom : {self.last_name}\nPrénom : {self.first_name}\nSexe : {str.upper(self.sex)}\nAnniversaire : {self.birthday}\nClassement : {self.rating}"
