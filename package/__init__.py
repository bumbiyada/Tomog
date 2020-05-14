from flask import Flask, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.event import listens_for
from jinja2 import Markup
from flask_security import SQLAlchemyUserDatastore, Security, current_user
from flask_admin import Admin, AdminIndexView, form
from flask_admin.contrib import sqla
import os
import os.path as op
from package.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

file_path = op.join(op.dirname(__file__), 'static')
try:
    os.mkdir(file_path)
except OSError:
    pass



#from models import Manufactures, XrayTubes, User, Role, Tables
from package.models import *
from package.routes import *

@listens_for(Image, 'after_delete')
def del_image(mapper, connection, target):
    if target.path:
        # Delete image
        try:
            os.remove(op.join(file_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(file_path,
                              form.thumbgen_filename(target.path)))
        except OSError:
            pass

#from package import Xraytubes, Manufactures
# Admin #

class AdminMixin():
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))

class Adminview(AdminMixin,sqla.ModelView):
    pass

class Homeadmin(AdminMixin,AdminIndexView):
    pass

class Tubeadminview(AdminMixin,sqla.ModelView):
    form_columns = ['manufacture', 'tube_model', 'focus', 'capacity', 'coolingrate', 'servise_life']

class Tableadminview(AdminMixin,sqla.ModelView):
    form_columns = ['manufacture', 'table_name', 'horizont_range', 'max_weight']

class Generatoradminview(AdminMixin,sqla.ModelView):
    form_columns = ['manufacture', 'generator_name', 'power', 'current', 'voltage']

class Manufactureadminview(AdminMixin,sqla.ModelView):
    form_columns = ['manufacture_name', 'manufacture_longname', 'country']

class Technoadminview(AdminMixin,sqla.ModelView):
    form_columns = ['manufacture', 'technology_name', 'technology_text', 'category']

class Tomogadminview(AdminMixin,sqla.ModelView):
    form_columns = ['manufacture', 'tomog_model', 'spiraltype', 'tubecount', 'gantry', 'slicecount', 'slice_thicness', 'fov_x',
                    'fov_z', 'spatial_resolution', 'rotation_time', 'fps', 'generator', 'table', 'tube', 'room_size',
                    'performance', 'technologies', 'image']

class ImageView(AdminMixin,sqla.ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.path)))


    column_formatters = {
        'path': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': form.ImageUploadField('Image',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True))
    }





admin = Admin(app, 'На сайт', url='/', index_view=Homeadmin(name='Home'))
#admin = Admin(app)


admin.add_view(Tomogadminview(Tomog, db.session))
admin.add_view(Manufactureadminview(Manufactures, db.session))
admin.add_view(Tubeadminview(Tubes, db.session))
admin.add_view(Generatoradminview(Generator, db.session))
admin.add_view(Tableadminview(Tables, db.session))
admin.add_view(ImageView(Image, db.session))

admin.add_view(Adminview(Hints, db.session))
admin.add_view(Technoadminview(Technologies, db.session))

# security #
user_datastore = SQLAlchemyUserDatastore(db,User, Role)
security = Security(app, user_datastore)

db.create_all()

