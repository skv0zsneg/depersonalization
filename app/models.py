from app import db
from sqlalchemy.orm import backref


class TestData(db.Model):
    """Модель тестовых данных студентов."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    middle_name = db.Column(db.String, nullable=False)
    birth_place = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    doc_serial = db.Column(db.String, nullable=False)
    doc_number = db.Column(db.String, nullable=False)
    inn = db.Column(db.String, nullable=False)
    snils = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    family_status = db.Column(db.String, nullable=False)
    group_number = db.Column(db.String, nullable=False)
    institute_name = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        super(TestData, self).__init__(**kwargs)


class Method(db.Model):
    """Модель, содержащая названия используемых
    в приложении методов обезличивания."""
    id = db.Column(db.Integer, primary_key=True)
    method_name = db.Column(db.String(128), nullable=False)


class CalculateData(db.Model):
    """Модель, содержащая данные для будующих
    раcсчетов эффективности методов обезличивания и
    деобезличивания."""
    id = db.Column(db.Integer, primary_key=True)
    time_to_ob = db.Column(db.String(256), nullable=False)
    time_to_deob = db.Column(db.String(256), nullable=False)

    method_id = db.Column(db.Integer, db.ForeignKey(
        'method.id'), nullable=False)
    method = db.relationship(
        'Method', backref=db.backref('calculate_datas', lazy=True))


db.create_all()
