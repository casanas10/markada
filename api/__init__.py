from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# ENV = 'dev'
ENV = 'prod'

if ENV == 'dev':
    from config import Config
    app.config.from_object(Config)
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ["SQLALCHEMY_TRACK_MODIFICATIONS"]
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

db = SQLAlchemy(app)
ma = Marshmallow(app)

import api.views, api.models

db.create_all()
