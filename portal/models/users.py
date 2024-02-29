from . import db
from datetime import datetime
from sqlalchemy import Sequence


class Users(db.Model):
    __bind_key__ = 'db'

    id = db.Column(db.Integer, Sequence('users_sequence'), unique=True, nullable=False, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email_id = db.Column(db.String(255))
    role = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    type_organization = db.Column(db.String(255), nullable=False)
    organization_name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=False)
    create_by = db.Column(db.String(255), nullable=False)
    access_to_admin = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_date = db.Column(db.TIMESTAMP, default=datetime.now)

    attributes_1 = db.Column(db.String(255))
    attributes_2 = db.Column(db.String(255))
    attributes_3 = db.Column(db.String(255))
    attributes_4 = db.Column(db.String(255))
    attributes_5 = db.Column(db.String(255))
    attributes_6 = db.Column(db.String(255))
    attributes_7 = db.Column(db.String(255))
    attributes_8 = db.Column(db.String(255))
    attributes_9 = db.Column(db.String(255))
    attributes_10 = db.Column(db.String(255))
    attributes_11 = db.Column(db.String(255))
    attributes_12 = db.Column(db.String(255))
    attributes_13 = db.Column(db.String(255))
    attributes_14 = db.Column(db.String(255))
    attributes_15 = db.Column(db.String(255))
    attributes_16 = db.Column(db.String(255))
    attributes_17 = db.Column(db.String(255))
    attributes_18 = db.Column(db.String(255))
    attributes_19 = db.Column(db.String(255))
    attributes_20 = db.Column(db.String(255))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
