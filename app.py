from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
@app.route("/start_testing")
def description():
    return render_template('testing_page.html')
