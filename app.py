from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
@app.route("/creating-test-db")
def testing_methods():
    return render_template('creating_test_db.html')


@app.route("/method-1")
def method_1():
    return render_template('method_1.html')


@app.route("/method-2")
def method_2():
    return render_template('method_2.html')


@app.route("/method-3")
def method_3():
    return render_template('method_3.html')


@app.route("/summary")
def summary():
    return render_template('summary.html')
