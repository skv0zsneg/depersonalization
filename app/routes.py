from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import TestData, CalculateData, Method
from app.repositories import generate_random_persons


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
    
