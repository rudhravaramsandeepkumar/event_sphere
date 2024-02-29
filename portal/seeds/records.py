from .. import LOG
from ..models.input_types import InputTypes


class AddInput:
    def __init__(self, db):
        self.db = db

    def run(self):
        self.create_input_types()
        try:
            self.db.session.commit()
        except Exception as e:
            LOG.error(e)

    def create_input_types(self):
        user1 = InputTypes(unique_id='59836',
                           input_type='Textbook',
                           type_id='1',
                           status='Y')
        user2 = InputTypes(unique_id='59837',
                           input_type='DropDown',
                           type_id='2',
                           status='Y')
        user3 = InputTypes(unique_id='59838',
                           input_type='Date',
                           type_id='3',
                           status='Y')
        user4 = InputTypes(unique_id='59839',
                           input_type='textarea',
                           type_id='4',
                           status='Y')

        self.db.session.merge(user1)
        self.db.session.merge(user2)
        self.db.session.merge(user3)
        self.db.session.merge(user4)
