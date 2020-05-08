from flask import Flask, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from package.config import Config
from flask_security import SQLAlchemyUserDatastore, Security, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
#from models import Manufactures, XrayTubes, User, Role, Tables
from package.routes import *
from package.models import *
#from package import Xraytubes, Manufactures
# Admin #

class AdminMixin():
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))

class Adminview(AdminMixin,ModelView):
    pass

class Homeadmin(AdminMixin,AdminIndexView):
    pass

class Tubeadminview(AdminMixin,ModelView):
    form_columns = ['manufacture', 'model', 'focus', 'capacity', 'coolingrate', 'servise_life']

class Tableadminview(AdminMixin,ModelView):
    form_columns = ['manufacture', 'name', 'horizont_range', 'max_weight']

class Generatoradminview(AdminMixin,ModelView):
    form_columns = ['manufacture', 'name', 'power', 'current', 'voltage']

class Manufactureadminview(AdminMixin,ModelView):
    form_columns = ['name', 'longname', 'country']

class Technoadminview(AdminMixin,ModelView):
    form_columns = ['manufacture', 'name', 'text', 'category']

class Tomogadminview(AdminMixin,ModelView):
    form_columns = ['manufacture', 'model', 'spiraltype', 'tubecount', 'gantry', 'slicecount', 'slice_thicness', 'fov_x',
                    'fov_z', 'spatial_resolution', 'rotation_time', 'fps', 'generator', 'table', 'tube', 'room_size',
                    'performance', 'technologies']

admin = Admin(app, 'GoToHomepage', url='/', index_view=Homeadmin(name='Home'))
admin.add_view(Tomogadminview(Tomog, db.session))
admin.add_view(Tubeadminview(Tubes, db.session))
admin.add_view(Manufactureadminview(Manufactures, db.session))
admin.add_view(Tableadminview(Tables, db.session))
admin.add_view(Generatoradminview(Generator, db.session))
admin.add_view(Technoadminview(Technologies, db.session))
admin.add_view(Adminview(Hints, db.session))

# security #
user_datastore = SQLAlchemyUserDatastore(db,User, Role)
security = Security(app, user_datastore)

db.create_all()

