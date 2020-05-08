from package import db
from flask_security import UserMixin, RoleMixin


role_user = db.Table('role_user',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                     )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128),)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=role_user, backref=db.backref('user', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(255))


class Tubes(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    manufacture_id = db.Column(db.Integer, db.ForeignKey('manufactures.id'), nullable=False)
    model = db.Column(db.String(128), nullable=False)
    focus = db.Column(db.String(128))
    capacity = db.Column(db.Float())
    coolingrate = db.Column(db.Float())
    servise_life = db.Column(db.Integer())
    tomog = db.relationship('Tomog', backref='tube', lazy=True)


class Manufactures(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    longname = db.Column(db.String(255))
    country = db.Column(db.String(128))
    tubes = db.relationship('Tubes', backref='manufacture', lazy=True)
    generators = db.relationship('Generator', backref='manufacture', lazy=True)
    tables = db.relationship('Tables', backref='manufacture', lazy=True)
    technologies = db.relationship('Technologies', backref='manufacture', lazy=True)
    tomog = db.relationship('Tomog', backref='manufacture', lazy=True)

    def __repr__(self):
        return '{}'.format(self.name)


class Tables(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    manufacture_id = db.Column(db.Integer, db.ForeignKey('manufactures.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    horizont_range = db.Column(db.Integer())
    max_weight = db.Column(db.Integer())
    tomog = db.relationship('Tomog', backref='table', lazy=True)


class Generator(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    manufacture_id = db.Column(db.Integer, db.ForeignKey('manufactures.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    power = db.Column(db.Integer())
    current = db.Column(db.Integer())
    voltage = db.Column(db.Integer())
    tomog = db.relationship('Tomog', backref='generator', lazy=True)

tomog_techno = db.Table('tomog_techno',
                     db.Column('tomog_id', db.Integer, db.ForeignKey('tomog.id')),
                     db.Column('techno_id', db.Integer, db.ForeignKey('technologies.id'))
                     )


class Technologies(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    manufacture_id = db.Column(db.Integer, db.ForeignKey('manufactures.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text)
    category = db.Column(db.String(128))


class Hints(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text)


class Tomog(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    manufacture_id = db.Column(db.Integer, db.ForeignKey('manufactures.id'), nullable=False)
    model = db.Column(db.String(128), nullable=False)
    spiraltype = db.Column(db.String(128))
    tubecount = db.Column(db.String(128))
    gantry = db.Column(db.Integer())
    slicecount = db.Column(db.Integer())
    slice_thicness = db.Column(db.Float())
    fov_x = db.Column(db.Integer())
    fov_z = db.Column(db.Integer())
    spatial_resolution = db.Column(db.Float())
    rotation_time = db.Column(db.Float())
    fps = db.Column(db.Integer())
    room_size = db.Column(db.Float())
    performance = db.Column(db.Float())
    tube_id = db.Column(db.Integer, db.ForeignKey('tubes.id'), nullable=False)
    generator_id = db.Column(db.Integer, db.ForeignKey('generator.id'), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=False)
    technologies = db.relationship('Technologies', secondary=tomog_techno, backref=db.backref('tomog', lazy='dynamic'))
