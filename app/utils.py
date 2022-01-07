from random import choice, randint
from typing import Optional
from string import digits
from mimesis.enums import Gender


def generate_random_group() -> str:
    letters = "АБВГДЕЖЗИКЛМНОПРСТУФХЦ"
    digits = "123456789"
    group = f"{choice(letters)}{choice(letters)}{choice(letters)}{choice(letters)}-0{choice(digits)}-2{choice(digits)}"

    return group


def generate_random_institute_name() -> str:
    institutes = [
        "Институт информационных технологий",
        "Институт искусственного интеллекта",
        "Институт кибербезопасности и цифровых технологий",
        "Институт перспективных технологий и индустриального программирования",
        "Институт радиоэлектроники и информатики",
        "Институт технологий управления",
        "Институт тонких химических технологий им. М.В. Ломоносова",
    ]
    return choice(institutes)


def get_mimesis_enum_gender(str_gender: str) -> Gender:
    if str_gender.upper() == "ЖЕН.":
        return Gender.FEMALE
    return Gender.MALE


def get_random_date(year_from: int = 1980, year_to: int = 2004) -> str:
    return f"{randint(1, 28)}.{randint(1, 12)}.{randint(year_from, year_to)}"


def get_military_data(str_gender: str) -> Optional[str]:
    if str_gender.upper() == "ЖЕН.":
        return None
    return choice(["Годен к военной службе.", "Не годен к военной службе."])


def get_payment_account() -> str:
    res = ''.join([choice(digits) for _ in range(20)])
    return res
