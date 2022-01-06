from app import db


class TableForShuffleMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.String, nullable=False)
    birth_place = db.Column(db.String, nullable=False)
    post_address = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    passport_serial = db.Column(db.String, nullable=False)
    passport_number = db.Column(db.String, nullable=False)
    inn = db.Column(db.String, nullable=False)
    snils = db.Column(db.String, nullable=False)
    telephone = db.Column(db.String, nullable=False)
    military_data = db.Column(db.String, nullable=True)
    family_status = db.Column(db.String, nullable=False)
    payment_account = db.Column(db.String, nullable=False)
    study_group_number = db.Column(db.String, nullable=False)
    study_institute = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        super(TableForShuffleMethod, self).__init__(**kwargs)


class UnDepersonalizationDataForShuffleMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.String, nullable=False)
    birth_place = db.Column(db.String, nullable=False)
    post_address = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    passport_serial = db.Column(db.String, nullable=False)
    passport_number = db.Column(db.String, nullable=False)
    inn = db.Column(db.String, nullable=False)
    snils = db.Column(db.String, nullable=False)
    telephone = db.Column(db.String, nullable=False)
    military_data = db.Column(db.String, nullable=True)
    family_status = db.Column(db.String, nullable=False)
    payment_account = db.Column(db.String, nullable=False)
    study_group_number = db.Column(db.String, nullable=False)
    study_institute = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        super(UnDepersonalizationDataForShuffleMethod, self).__init__(**kwargs)


db.create_all()
