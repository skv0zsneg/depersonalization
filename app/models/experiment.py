from app import db


class TestData(db.Model):
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
        super(TestData, self).__init__(**kwargs)


class ExperimentalData(db.Model):
    experimental_data_id = db.Column(db.Integer, primary_key=True)
    method_name = db.Column(db.String(256), nullable=False)
    time_to_depersonalization = db.Column(db.String(256), nullable=False)
    time_to_undepersonalization = db.Column(db.String(256), nullable=False)

    def __init__(self, **kwargs):
        super(ExperimentalData, self).__init__(**kwargs)


db.create_all()

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