from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
@app.route("/description")
def description():
    return render_template('index.html')

@app.route("/test-stand")
def test_stand():
    return render_template('test_stand.html')
