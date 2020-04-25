from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import redis
from rq import Queue

import os, enum

# Init
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'our-secret'

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
r = redis.Redis()
q = Queue(connection=r)

from app import routes