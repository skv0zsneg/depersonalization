from typing import Tuple
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from mimesis import Person, Address
from mimesis.locales import Locale
from mimesis.builtins import RussiaSpecProvider
from random import choice

import sqlalchemy
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
                                                                           fio=person.fio,
                                                                           passport_number=person.passport_number)[0]
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


# Метод перемешивания
def run_depersonalization_shuffle(db: SQLAlchemy) -> None:
    db.session.query(TableForShuffleMethod).delete()
    db.session.query(UnDepersonalizationDataForShuffleMethod).delete()

    for i in range(len(db.session.query(TestData).all())):
        desc_person = db.session.query(
            TestData).order_by(TestData.fio.desc())[i]
        asc_person = db.session.query(TestData).order_by(TestData.fio.asc())[i]
        db.session.add(
            TableForShuffleMethod(
                fio=asc_person.fio,
                birth_date=desc_person.birth_date,
                birth_place=asc_person.birth_place,
                post_address=desc_person.post_address,
                email=asc_person.email,
                passport_serial=desc_person.passport_serial,
                passport_number=asc_person.passport_number,
                inn=desc_person.inn,
                snils=asc_person.snils,
                telephone=desc_person.telephone,
                military_data=asc_person.military_data,
                family_status=desc_person.family_status,
                payment_account=asc_person.payment_account,
                study_group_number=desc_person.study_group_number,
                study_institute=asc_person.study_institute,
            )
        )

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


def run_undepersonalization_shuffle(db: SQLAlchemy) -> None:
    for i in range(len(db.session.query(TestData).all())):
        shuffle_person = db.session.query(TableForShuffleMethod).all()[i]
        desc_shuffle_person = db.session.query(TableForShuffleMethod).order_by(
            TableForShuffleMethod.fio.desc())[i]

        db.session.add(
            UnDepersonalizationDataForShuffleMethod(
                fio=desc_shuffle_person.fio,
                birth_date=shuffle_person.birth_date,
                birth_place=desc_shuffle_person.birth_place,
                post_address=shuffle_person.post_address,
                email=desc_shuffle_person.email,
                passport_serial=shuffle_person.passport_serial,
                passport_number=desc_shuffle_person.passport_number,
                inn=shuffle_person.inn,
                snils=desc_shuffle_person.snils,
                telephone=shuffle_person.telephone,
                military_data=desc_shuffle_person.military_data,
                family_status=shuffle_person.family_status,
                payment_account=desc_shuffle_person.payment_account,
                study_group_number=shuffle_person.study_group_number,
                study_institute=desc_shuffle_person.study_institute,
            )
        )

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


# Метод Декомпозиции
def run_depersonalization_decomposition(db: SQLAlchemy) -> None:
    db.session.query(FirstDepersonalizeTableForDecompositionMethod).delete()
    db.session.query(SecondDepersonalizeTableForDecompositionMethods).delete()
    db.session.query(LinkTableForDecompositionMethod).delete()

    for person in db.session.query(TestData).all():
        db.session.add(
            FirstDepersonalizeTableForDecompositionMethod(
                military_data=person.military_data,
                family_status=person.family_status,
                study_institute=person.study_institute
            )
        )
        db.session.add(
            SecondDepersonalizeTableForDecompositionMethods(
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
        cur_person_2_table = SecondDepersonalizeTableForDecompositionMethods().query.filter_by(payment_account=person.payment_account,
                                                                                               fio=person.fio,
                                                                                               passport_number=person.passport_number)[0]
        db.session.add(
            LinkTableForDecompositionMethod(
                first_table_identifier=cur_person_2_table.id,
                second_table_identifier=cur_person_2_table.id
            )
        )

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


def run_undepersonalization_decomposition(db: SQLAlchemy) -> None:
    for link in db.session.query(LinkTableForDecompositionMethod).all():
        table_1 = db.session.query(FirstDepersonalizeTableForDecompositionMethod).filter_by(
            id=link.first_table_identifier
        )[0]
        table_2 = db.session.query(SecondDepersonalizeTableForDecompositionMethods).filter_by(
            id=link.second_table_identifier
        )[0]
        db.session.add(
            UnDepersonalizationDataForDecompositionMethod(
                fio=table_2.fio,
                birth_date=table_2.birth_date,
                birth_place=table_2.birth_place,
                post_address=table_2.post_address,
                email=table_2.email,
                passport_serial=table_2.passport_serial,
                passport_number=table_2.passport_number,
                inn=table_2.inn,
                snils=table_2.snils,
                telephone=table_2.telephone,
                military_data=table_1.military_data,
                family_status=table_1.family_status,
                payment_account=table_2.payment_account,
                study_group_number=table_2.study_group_number,
                study_institute=table_1.study_institute,
            )
        )

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


def calculate(db: SQLAlchemy,
              method_name: str) -> Tuple[str, str, str]:
    """Рассчет критериев эффективности.

    :return: Скорость обезличивания, скорость деобезличивания, 
    критерий совместимости, размер (в байтах) тестовых данных.
    """
    t_de = float(db.session.query(ExperimentalData).filter_by(
        method_name=method_name).first().time_to_depersonalization
    )
    t_unde = float(db.session.query(ExperimentalData).filter_by(
        method_name=method_name).first().time_to_undepersonalization
    )
    test_data_size = 0
    for person in db.session.query(TestData).all():
        test_data_size += len(person.fio.encode('utf-8'))
        test_data_size += len(person.birth_date.encode('utf-8'))
        test_data_size += len(person.birth_place.encode('utf-8'))
        test_data_size += len(person.post_address.encode('utf-8'))
        test_data_size += len(person.email.encode('utf-8'))
        test_data_size += len(person.passport_serial.encode('utf-8'))
        test_data_size += len(person.passport_number.encode('utf-8'))
        test_data_size += len(person.inn.encode('utf-8'))
        test_data_size += len(person.snils.encode('utf-8'))
        test_data_size += len(person.telephone.encode('utf-8'))
        test_data_size += len(person.military_data.encode('utf-8')) if person.military_data is not None else 0
        test_data_size += len(person.family_status.encode('utf-8'))
        test_data_size += len(person.payment_account.encode('utf-8'))
        test_data_size += len(person.study_group_number.encode('utf-8'))
        test_data_size += len(person.study_institute.encode('utf-8'))
        
    de_speed = test_data_size / t_de if t_de != 0 else 0
    unde_speed = test_data_size / t_unde if t_unde != 0 else 0
    compibility = de_speed - unde_speed

    return str(round(de_speed, 1)), str(round(unde_speed, 1)), str(round(compibility, 1)), str(test_data_size)
