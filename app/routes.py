from time import perf_counter
from flask import render_template, request, redirect, url_for
from app import app, db
from app.repositories import generate_random_persons
from app.models.experiment import TestData, ExperimentalData


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
    # ...
    return redirect(url_for("testing_methods"))


@app.route("/run-method-1", methods=['GET'])
def run_method_1():
    # ...
    db.session.commit()


@app.route("/run-method-2", methods=['GET'])
def run_method_2():
    # ...
    db.session.commit()


@app.route("/run-method-3", methods=['GET'])
def run_method_3():
    # ...
    db.session.commit()
