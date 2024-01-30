from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .entity.db import db

app = Flask(__name__)
app.config.from_object('testapp.config')
db.init_app(app)
migrate = Migrate(app, db)

from .entity import employee
from.entity import pairs
from.entity import users
from.entity import has_sent

import testapp.views