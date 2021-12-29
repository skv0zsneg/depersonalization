from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['main_db_url']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from app import routes, repositories, utils
from app.models import main, ex_identifiers