from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models.employee import db

app = Flask(__name__)
app.config.from_object('testapp.config')
db.init_app(app)
migrate = Migrate(app, db)

from .models import employee

import testapp.views