import sqlalchemy
from .base import metadata


test_data = sqlalchemy.Table(
    "test_data",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.INTEGER, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column('first_name', sqlalchemy.String),
    sqlalchemy.Column('second_name', sqlalchemy.String),
    sqlalchemy.Column('middle_name', sqlalchemy.String),
    sqlalchemy.Column('date_of_birth', sqlalchemy.Date),
    sqlalchemy.Column('place_of_birth', sqlalchemy.String),
    sqlalchemy.Column('address', sqlalchemy.String),
    sqlalchemy.Column('mailing_address', sqlalchemy.String),
    sqlalchemy.Column('email', sqlalchemy.String),
    sqlalchemy.Column('doc_serial', sqlalchemy.String),
    sqlalchemy.Column('doc_number', sqlalchemy.String),
    sqlalchemy.Column('inn', sqlalchemy.String),
    sqlalchemy.Column('snils', sqlalchemy.String),
    sqlalchemy.Column('phone_number', sqlalchemy.String),
    # TODO: закончить модель.
)