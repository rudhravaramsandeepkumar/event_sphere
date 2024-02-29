from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(
)

def init_app(app):
    db_connection_string = ''
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_BINDS'] = {
        'db': "sqlite:///db.sqlite"
    }
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)
    app.logger.info('Initialized models')
    with app.app_context():
        from .events import Events
        from .events_eligible_users import EventsEligibleUsers
        from .users import Users
        from .users_type import UsersType
        from .input_types import InputTypes
        from .event_inputs import EventInputs
        from .event_inputs_info import EventInputsInfo
        from .event_inputs_dropdown_keys import EventInputDropdownKeys
        from .event_attendance import EventAttendance

        db.create_all()
        db.session.commit()
        app.logger.debug('All tables are created')

