from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from mimesis import Person, Address
from mimesis.locales import Locale
from mimesis.builtins import RussiaSpecProvider
from random import choice
from app import utils
from app.models.experiment import TestData, ExperimentalData
from app.models.identifier import (
    DepersonalizeDataForIdentifierMethod,
    ConformityTableForIdentifierMethod,
    UnDepersonalizationDataForIdentifierMethod,
)
from app.models.shuffle import (
    TableForShuffleMethod,
    UnDepersonalizationDataForShuffleMethod,
)
from app.models.decomposition import (
    FirstDepersonalizeTableForDecompositionMethod,
    SecondDepersonalizeTableForDecompositionMethods,
    LinkTableForDecompositionMethod,
    UnDepersonalizationDataForDecompositionMethod,
)


def clear_and_update_db(db: SQLAlchemy) -> None:
    db.session.query(TestData).delete()
    db.session.query(ExperimentalData).delete()

    db.session.query(DepersonalizeDataForIdentifierMethod).delete()
    db.session.query(ConformityTableForIdentifierMethod).delete()
    db.session.query(UnDepersonalizationDataForIdentifierMethod).delete()

    db.session.query(TableForShuffleMethod).delete()
    db.session.query(UnDepersonalizationDataForShuffleMethod).delete()

    db.session.query(FirstDepersonalizeTableForDecompositionMethod).delete()
    db.session.query(SecondDepersonalizeTableForDecompositionMethods).delete()
    db.session.query(LinkTableForDecompositionMethod).delete()
    db.session.query(UnDepersonalizationDataForDecompositionMethod).delete()

    for method_name in ['identifier', 'shuffle', 'decomposition']:
        db.session.add(
            ExperimentalData(
                method_name=method_name,
                time_to_depersonalization='0',
                time_to_undepersonalization='0'
            )
        )

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


def write_time_into_experimental_data(db: SQLAlchemy,
                                      t_de: float,
                                      t_unde: float,
                                      method: str) -> None:
    ExperimentalData().query.filter_by(method_name=method).update(
        {'time_to_depersonalization': str(t_de),
         'time_to_undepersonalization': str(t_unde)}
    )
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


def generate_random_persons(db: SQLAlchemy, person_count: str) -> None:
    clear_and_update_db(db)

    for _ in range(int(person_count)):
        person = Person(Locale.RU)
        rus_provider = RussiaSpecProvider()
        address = Address("ru")

        fio = f"{person.name()} {person.surname()} {rus_provider.patronymic(utils.get_mimesis_enum_gender(person.gender()))}"
        db.session.add(
            TestData(
                fio=fio,
                birth_date=utils.get_random_date(),
                birth_place=address.address(),
                post_address=address.address(),
                email=person.email(),
                passport_serial=rus_provider.passport_series(),
                passport_number=rus_provider.passport_number(),
                inn=rus_provider.inn(),
                snils=rus_provider.snils(),
                telephone=person.telephone(),
                military_data=utils.get_military_data(person.gender()),
                family_status=choice(
                    ["Не состоит в браке", "Состоит в браке"]),
                payment_account=utils.get_payment_account(),
                study_group_number=utils.generate_random_group(),
                study_institute=utils.generate_random_institute_name(),
            )
        )

        del person, rus_provider, address

        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()


# Метод идентификаторов
def run_depersonalization_identifier(db: SQLAlchemy) -> None:
    db.session.query(DepersonalizeDataForIdentifierMethod).delete()
    db.session.query(ConformityTableForIdentifierMethod).delete()
    db.session.query(UnDepersonalizationDataForIdentifierMethod).delete()

    for person in db.session.query(TestData).all():
        db.session.add(
            ConformityTableForIdentifierMethod(
                fio=person.fio,
                birth_date=person.birth_date,
                birth_place=person.birth_place,
                post_address=person.post_address,
                email=person.email,
                passport_serial=person.passport_serial,
                passport_number=person.passport_number,
                inn=person.inn,
                snils=person.snils,
                telephone=person.telephone,
                payment_account=person.payment_account,
                study_group_number=person.study_group_number
            )
        )

        curr_person = ConformityTableForIdentifierMethod().query.filter_by(payment_account=person.payment_account,
                                                                           fio=person.fio)[0]
        db.session.add(
            DepersonalizeDataForIdentifierMethod(
                military_data=person.military_data,
                family_status=person.family_status,
                study_institute=person.study_institute,
                conformity_table_for_identifier_method_id=curr_person.id
            )
        )
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()


def run_un_depersonalization_identifier(db: SQLAlchemy) -> None:
    for dep_person in db.session.query(DepersonalizeDataForIdentifierMethod).all():
        con_person = ConformityTableForIdentifierMethod().query.filter_by(
            id=dep_person.conformity_table_for_identifier_method_id
        )[0]
        db.session.add(
            UnDepersonalizationDataForIdentifierMethod(
                fio=con_person.fio,
                birth_date=con_person.birth_date,
                birth_place=con_person.birth_place,
                post_address=con_person.post_address,
                email=con_person.email,
                passport_serial=con_person.passport_serial,
                passport_number=con_person.passport_number,
                inn=con_person.inn,
                snils=con_person.snils,
                telephone=con_person.telephone,
                military_data=dep_person.military_data,
                family_status=dep_person.family_status,
                payment_account=con_person.payment_account,
                study_group_number=con_person.study_group_number,
                study_institute=dep_person.study_institute,
            )
        )
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
