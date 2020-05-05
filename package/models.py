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


class XrayTubes(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    model = db.Column(db.String(128), nullable=False)
    focus = db.Column(db.String(128))
    capacity = db.Column(db.Float())
    coolingrate = db.Column(db.Float())
    servise_life = db.Column(db.Integer())


class Manufactures(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    longname = db.Column(db.String(255))
    country = db.Column(db.String(128))


class Tables(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    horizont_range = db.Column(db.Integer())
    max_weight = db.Column(db.Integer())


class Generator(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    power = db.Column(db.Integer())
    current = db.Column(db.Integer())
    voltage = db.Column(db.Integer())
