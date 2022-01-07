from app import db


class FirstDepersonalizeTableForDecompositionMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    military_data = db.Column(db.String, nullable=True)
    family_status = db.Column(db.String, nullable=False)
    study_institute = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        super(FirstDepersonalizeTableForDecompositionMethod, self).__init__(**kwargs)


class SecondDepersonalizeTableForDecompositionMethods(db.Model):
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
    payment_account = db.Column(db.String, nullable=False)
    study_group_number = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        super(SecondDepersonalizeTableForDecompositionMethods, self).__init__(**kwargs)


class LinkTableForDecompositionMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_table_identifier = db.Column(db.String, nullable=False)
    second_table_identifier = db.Column(db.String, nullable=False)

class UnDepersonalizationDataForDecompositionMethod(db.Model):
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
        super(UnDepersonalizationDataForDecompositionMethod, self).__init__(**kwargs)


db.create_all()
