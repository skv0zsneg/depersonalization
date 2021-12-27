from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def testing_methods():
    if request.method == 'POST':
        pass
    else:
        return render_template('creating_test_db.html')


@app.route("/method-1", methods=['POST', 'GET'])
def method_1():
    return render_template('method_1.html')


@app.route("/method-2", methods=['POST', 'GET'])
def method_2():
    return render_template('method_2.html')


@app.route("/method-3", methods=['POST', 'GET'])
def method_3():
    return render_template('method_3.html')


@app.route("/summary")
def summary():
    return render_template('summary.html')
