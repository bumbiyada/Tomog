from package import db, user_datastore
from package.models import *
user_datastore.create_user(email='admin@mail.com', name='admin', password='admin')
user_datastore.create_role(name='admin', description='administrator')
user = User.query.first()
role = Role.query.first()
user_datastore.add_role_to_user(user, role)
db.session.commit()


