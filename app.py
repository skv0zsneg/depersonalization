from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
@app.route("/creating-test-db")
def testing_methods():
    return render_template('creating_test_db.html')


@app.route("/1-method")
def method_1():
    return render_template('fst_dp_method.html')


@app.route("/2-method")
def method_2():
    return render_template('scd_dp_method.html')


@app.route("/3-method")
def method_3():
    return render_template('thrd_dp_method.html')


@app.route("/summary")
def summary():
    return render_template('summary.html')
