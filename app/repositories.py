from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from mimesis import Person, Address
from mimesis.locales import Locale
from mimesis.builtins import RussiaSpecProvider
from random import choice
from typing import Optional
from app.models.main import TestData
from app import utils


def generate_random_persons(db: SQLAlchemy, person_count: str) -> None:
    db.session.delete
    for _ in range(int(person_count)):
        person = Person(Locale.RU)
        rus_provider = RussiaSpecProvider()
        address = Address('ru')

        db.session.add(TestData(
            name=person.name(),
            surname=person.surname(),
            middle_name=rus_provider.patronymic(
                utils.get_mimesis_enum_gender(person.gender())
            ),
            birth_place=address.address(),
            address=address.address(),
            email=person.email(),
            doc_serial=rus_provider.passport_series(),
            doc_number=rus_provider.passport_number(),
            inn=rus_provider.inn(),
            snils=rus_provider.snils(),
            phone_number=person.telephone(),
            family_status=choice(['Не состоит в браке', 'Состоит в браке']),
            group_number=utils.generate_random_group(),
            institute_name=utils.generate_random_institute_name()
        ))

        del person, rus_provider, address

        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
