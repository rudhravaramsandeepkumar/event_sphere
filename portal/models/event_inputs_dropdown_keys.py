from datetime import datetime
from . import db
from sqlalchemy import Sequence


class EventInputDropdownKeys(db.Model):
    __bind_key__ = 'db'

    id = db.Column(db.Integer, Sequence('event_inputs_keys_dropdown_sequence'), unique=True, nullable=False, primary_key=True)
    event_id = db.Column(db.String(255), nullable=False)
    event_inputs_id = db.Column(db.String(255), nullable=False)
    dropdown_value = db.Column(db.String(255))
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
    attributes_21 = db.Column(db.String(255))
    attributes_22 = db.Column(db.String(255))
    attributes_23 = db.Column(db.String(255))
    attributes_24 = db.Column(db.String(255))
    attributes_25 = db.Column(db.String(255))
    attributes_26 = db.Column(db.String(255))
    attributes_27 = db.Column(db.String(255))
    attributes_28 = db.Column(db.String(255))
    attributes_29 = db.Column(db.String(255))
    attributes_30 = db.Column(db.String(255))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
