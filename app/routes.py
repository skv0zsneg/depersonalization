from time import perf_counter
from flask import render_template, request, redirect, url_for
from app import app, db
from app.repositories import generate_random_persons
from app.models.main import TestData, CalculateData
from app.models.ex_identifiers import ExDepersonalizeTestDataMethodIdentifiers, ExIdentifier


# -- pages ---
@app.route("/", methods=['GET'])
@app.route("/testing-methods", methods=['GET'])
def testing_methods():
    return render_template('creating_test_db.html', test_datas=TestData.query.all())


@app.route("/method-1", methods=['POST', 'GET'])
def method_1():
    return render_template('method_1.html')


@app.route("/method-2", methods=['POST', 'GET'])
def method_2():
    return render_template('method_2.html')


@app.route("/method-3", methods=['POST', 'GET'])
def method_3():
    return render_template('method_3.html')


@app.route("/summary", methods=['GET'])
def summary():
    return render_template('summary.html')


# -- actions ---
@app.route("/generate-persons", methods=['POST'])
def generate_persons():
    TestData.query.delete()
    db.session.commit()
    person_count = request.form['personCount']
    generate_random_persons(db, person_count)

    return redirect(url_for("testing_methods"))


@app.route("/run-method-1", methods=['GET'])
def run_method_1():
    ExDepersonalizeTestDataMethodIdentifiers.query.delete()
    ExIdentifier.query.delete()
    db.session.commit()

    t_start = perf_counter()
    # Обезличивание
    time_to_ob = perf_counter() - t_start

    t_start = perf_counter()
    # ДеОбезличивание
    time_to_deob = perf_counter() - t_start

    db.session.add(CalculateData(
        time_to_ob=time_to_ob,
        time_to_deob=time_to_deob,
        method_name="Метод введения идентификаторов."
    ))
    db.session.commit()


@app.route("/run-method-2", methods=['GET'])
def run_method_2():
    # ExDepersonalizeTestDataMethodIdentifiers.query.delete()
    # ExIdentifier.query.delete()
    # db.session.commit()

    t_start = perf_counter()
    # Обезличивание
    time_to_ob = perf_counter() - t_start

    t_start = perf_counter()
    # ДеОбезличивание
    time_to_deob = perf_counter() - t_start

    db.session.add(CalculateData(
        time_to_ob=time_to_ob,
        time_to_deob=time_to_deob,
        method_name="Метод перемешивания."
    ))
    db.session.commit()


@app.route("/run-method-3", methods=['GET'])
def run_method_3():
    # ExDepersonalizeTestDataMethodIdentifiers.query.delete()
    # ExIdentifier.query.delete()
    # db.session.commit()

    t_start = perf_counter()
    # Обезличивание
    time_to_ob = perf_counter() - t_start

    t_start = perf_counter()
    # ДеОбезличивание
    time_to_deob = perf_counter() - t_start

    db.session.add(CalculateData(
        time_to_ob=time_to_ob,
        time_to_deob=time_to_deob,
        method_name="Метод декомпозиции."
    ))
    db.session.commit()
