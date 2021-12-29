from random import choice
from mimesis.enums import Gender


def generate_random_group() -> str:
    letters = 'АБВГДЕЖЗИКЛМНОПРСТУФХЦ'
    digits = '123456789'
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
        "Институт тонких химических технологий им. М.В. Ломоносова"
    ]
    return choice(institutes)


def get_mimesis_enum_gender(str_gender: str) -> Gender:
    if str_gender.upper() == 'ЖЕН.':
        return Gender.FEMALE
    return Gender.MALE
