from app import db
from sqlalchemy.orm import backref


class ExDepersonalizeTestDataMethodIdentifiers(db.Model):
    """Обезличенная модель данных для метода идентификаторов."""
    id = db.Column(db.Integer, primary_key=True)
    birth_place = db.Column(db.String, nullable=False)
    family_status = db.Column(db.String, nullable=False)
    institute_name = db.Column(db.String, nullable=False)

    identifier_id = db.Column(
        db.Integer, db.ForeignKey('ex_identifier.id'), nullable=False
    )
    method = db.relationship(
        'ExIdentifier', backref=db.backref('custom_id', lazy=True)
    )

    def __init__(self, **kwargs):
        super(ExDepersonalizeTestDataMethodIdentifiers, self).__init__(**kwargs)


class ExIdentifier(db.Model):
    """Модель, содержащая секретные данные 
    относящиеся к идентификаторам."""
    id = db.Column(db.Integer, primary_key=True)
    custom_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    middle_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    doc_serial = db.Column(db.String, nullable=False)
    doc_number = db.Column(db.String, nullable=False)
    inn = db.Column(db.String, nullable=False)
    snils = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    group_number = db.Column(db.String, nullable=False)


db.create_all()
