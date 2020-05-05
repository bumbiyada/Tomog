from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_security import SQLAlchemyUserDatastore, Security
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from package import models, routes

### Admin ###
admin = Admin(app)
#admin.add_view(ModelView(XrayTubes, db.session))
#admin.add_view(ModelView(Manufactures, db.session))
#admin.add_view(ModelView(Suitype, db.session))

# security
user_datastore = SQLAlchemyUserDatastore(db,User, Role)
security = Security(app, user_datastore)

db.create_all()

