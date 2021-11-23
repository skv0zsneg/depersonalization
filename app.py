from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
@app.route("/before_depersonalization")
def before_depersonalization():
    return render_template('base.html')

@app.route("/identifiers")
def identifiers():
    return render_template('base.html')
