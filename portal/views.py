import json
import os
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file, make_response, \
    Response, jsonify
from sqlalchemy.orm.exc import NoResultFound
from .models import db
from .models.events import Events
from .models.events_eligible_users import EventsEligibleUsers

from .models.users import Users
from .models.input_types import InputTypes
from .models.event_inputs import EventInputs
from .models.event_inputs_info import EventInputsInfo
from .models.event_inputs_dropdown_keys import EventInputDropdownKeys
from .models.events_eligible_users import EventsEligibleUsers
from .models.event_attendance import EventAttendance
from .models.users_type import UsersType
from sqlalchemy.orm.exc import NoResultFound
import threading
from . import APP, LOG, login_required
from werkzeug.utils import secure_filename
from .security.updated_jwt import jwt_required
import time
from .helpers import get_random_numbers

bp = Blueprint('view', __name__, url_prefix='/', template_folder="./templates", static_folder="./static")


@bp.before_request
def before_request():
    import flask
    import datetime
    flask.session.permanent = True
    bp.permanent_session_lifetime = datetime.timedelta(minutes=10)
    flask.session.modified = True


@bp.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    r.headers["server"] = ""
    return r


@bp.route('/', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        invalid_msg = "hidden"
        access_name = "hidden"
        access_pass = "hidden"
        return render_template('register_login.html', invalid_msg=invalid_msg
                               , access_name=access_name, access_pass=access_pass)
    if request.method == "POST":
        username = request.form.get('check_email')
        password = request.form.get('check_password')
        if username == '':
            invalid_msg = "hidden"
            access_name = ""
            access_pass = "hidden"
            return render_template("register_login.html", invalid_msg=invalid_msg, access_name=access_name,
                                   access_pass=access_pass)
        if password == '':
            invalid_msg = "hidden"
            access_name = "hidden"
            access_pass = ""
            return render_template("register_login.html", invalid_msg=invalid_msg, access_name=access_name,
                                   access_pass=access_pass)
        try:
            users = Users.query.filter_by(username=username, password=password).one()
            if users is not None:
                if users.status == 'A':
                    print('amnsbnasmnasbns', users.id)
                    session["user"] = users.id
                    session["event_organizer_id"] = users.organization_name
                    session["access_to_admin_status"] = users.access_to_admin
                    return redirect(url_for('view.home'))
        except NoResultFound:
            pass
        except Exception as e:
            LOG.error("Error occurred while login ")
            LOG.error(e, exc_info=True)
        finally:
            db.session.close()
        invalid_msg = ""
        access_name = "hidden"
        access_pass = "hidden"
        return render_template("register_login.html", invalid_msg=invalid_msg, access_name=access_name,
                               access_pass=access_pass)


@bp.route('/home', methods=["GET", "POST"])
@login_required
def home():
    user_id_get = session.get('user')
    user_organization_name_get = session.get('event_organizer_id')
    list_of_ids = []
    list_of_event_name = []
    list_of_created_date = []
    list_of_description = []
    list_of_event_status = []
    try:
        # event_ = Events.query.filter_by(event_organizer_id=user_id_get).all()
        top_3_events = Events.query.filter_by(event_organizer_id=user_id_get, event_status='In Progress').order_by(
            Events.updated_date.desc()).all()
        for event in top_3_events:
            list_of_event_name.append(event.event_name)
            list_of_created_date.append(event.created_date)
            list_of_description.append(event.event_description)
            list_of_event_status.append(event.event_status)
            list_of_ids.append(event.event_id)
    except NoResultFound:
        pass

    old_list_of_ids = []
    old_list_of_event_name = []
    old_list_of_created_date = []
    old_list_of_description = []
    old_list_of_event_status = []
    try:
        # event_ = Events.query.filter_by(event_organizer_id=user_id_get).all()
        # top_3_events_2 = Events.query.filter_by(event_organizer_id=user_id_get, event_status='Created').order_by(
        #     Events.updated_date.desc()).limit(3).all()
        top_3_events_2 = Events.query.filter_by(event_organizer_id=user_id_get, event_status='Created').order_by(
            Events.updated_date.desc()).all()
        for event_2 in top_3_events_2:
            old_list_of_event_name.append(event_2.event_name)
            old_list_of_created_date.append(event_2.created_date)
            old_list_of_description.append(event_2.event_description)
            old_list_of_event_status.append(event_2.event_status)
            old_list_of_ids.append(event_2.event_id)
    except NoResultFound:
        pass

    toattend_list_of_ids = []
    toattend_list_of_event_name = []
    toattend_list_of_created_date = []
    toattend_list_of_description = []
    toattend_list_of_event_status = []
    toattend_list_of_event_start_date = []
    try:
        users = Users.query.filter_by(id=user_id_get).one()
        li_ = []
        all_users = EventsEligibleUsers.query.all()
        for all_user in all_users:
            li_.append([all_user.event_id, all_user.event_organizer_id])
        event_to_attend = db.session.query(Events, EventsEligibleUsers).filter(
            EventsEligibleUsers.event_organizer_id != user_id_get,
            EventsEligibleUsers.event_organization_id == user_organization_name_get,
            EventsEligibleUsers.event_eligible_candidates_role_id == users.role,
            EventsEligibleUsers.event_eligible_candidates_dep_id == users.department,
            Events.event_status == 'In Progress').outerjoin(EventsEligibleUsers,
                                                            Events.event_id == EventsEligibleUsers.event_id,
                                                            isouter=True).all()
        for ev_ent, Evn_elg in event_to_attend:
            toattend_list_of_event_name.append(ev_ent.event_name)
            toattend_list_of_created_date.append(ev_ent.created_date)
            toattend_list_of_description.append(ev_ent.event_description)
            toattend_list_of_event_status.append(ev_ent.event_status)
            toattend_list_of_ids.append(ev_ent.event_id)
            toattend_list_of_event_start_date.append(ev_ent.event_registration_start_date)
    except Exception as e:
        LOG.info(e)
        pass
    access_to_admin_status = session.get('access_to_admin_status')

    if access_to_admin_status == "No":
        access_to_admin_status_hidden = "hidden"
    else:
        access_to_admin_status_hidden = 'unset'
    return render_template('home.html', user_organization_name_get=user_organization_name_get,
                           list_of_event_name=list_of_event_name, list_of_created_date=list_of_created_date,
                           list_of_description=list_of_description, list_of_event_status=list_of_event_status,
                           list_of_ids=list_of_ids,
                           old_list_of_ids=old_list_of_ids, old_list_of_event_name=old_list_of_event_name,
                           old_list_of_created_date=old_list_of_created_date,
                           old_list_of_description=old_list_of_description,
                           old_list_of_event_status=old_list_of_event_status,
                           toattend_list_of_event_name=toattend_list_of_event_name,
                           toattend_list_of_created_date=toattend_list_of_created_date,
                           toattend_list_of_description=toattend_list_of_description,
                           toattend_list_of_event_status=toattend_list_of_event_status,
                           toattend_list_of_ids=toattend_list_of_ids,
                           toattend_list_of_event_start_date=toattend_list_of_event_start_date,
                           access_to_admin_status_hidden=access_to_admin_status_hidden)


@bp.route('/registration', methods=["GET", "POST"])
def registration():
    data = request.json
    print(data)
    head = Users(first_name=data['FirstName'],
                 last_name=data['LastName'],
                 username=data['userName'],
                 password=data['create_password'],
                 email_id=data['mail_id'],
                 role=data['role'],
                 department=data['department'],
                 type_organization=data['org_type'],
                 organization_name=data['org_name'],
                 status='A',
                 create_by="Admin",
                 access_to_admin="Yes")
    try:
        db.session.add(head)
        db.session.commit()
        db.session.close()
        msg = "successfully registered"
        Status = {"status": msg}
        print('Status', Status)
        return jsonify(Status)
    except Exception as e:
        LOG.error(e, exc_info=True)
        db.session.rollback()
        LOG.error("Error while pushing data")
        msg = "Failed, Please check the details"
        Status = {"status": msg}
        return jsonify(Status)


@bp.route('/check', methods=["GET", "POST"])
def enc_key():
    data = request.json
    print(data)
    reg_username = data['reg_username']
    print('reg_username', reg_username)
    reg_email = data['reg_email']
    print(data)
    try:
        users = Users.query.filter_by(username=reg_username).one()
        print(users.username)
        msg = ''
        if users is not None:
            msg = "user_name"
            return jsonify({"msg": msg})
    except NoResultFound:
        pass
    except Exception as e:
        LOG.error("Error occurred while login ")
        LOG.error(e, exc_info=True)
    finally:
        db.session.close()
    try:
        users2 = Users.query.filter_by(email_id=reg_email).one()
        if users2 is not None:
            msg = "email_id"
            return jsonify({
                "msg": msg})
        else:
            msg = "clear"
            return jsonify({
                "msg": msg})
    except NoResultFound:
        pass
    except Exception as e:
        LOG.error("Error occurred while login ")
        LOG.error(e, exc_info=True)
    finally:
        db.session.close()
    Status = {"msg": "msg"}
    return jsonify(Status)


@bp.route('/get_users', methods=["GET", "POST"])
def get_all_users_json():
    # Query all users
    all_users = Users.query.all()
    if all_users:
        users_as_json = [user.as_dict() for user in all_users]
        return jsonify(users_as_json)
    else:
        return jsonify([])


@bp.route('/get_events', methods=["GET", "POST"])
def get_events():
    # Query all users
    all_users = Events.query.all()
    if all_users:
        users_as_json = [user.as_dict() for user in all_users]
        return jsonify(users_as_json)
    else:
        return jsonify([])


@bp.route('/input_types', methods=["GET", "POST"])
def input_types():
    # Query all users
    all_users = InputTypes.query.all()
    if all_users:
        users_as_json = [user.as_dict() for user in all_users]
        return jsonify(users_as_json)
    else:
        return jsonify([])


@bp.route('/event_Inputs_get', methods=["GET", "POST"])
def event_Inputs_get():
    # Query all users
    all_users = EventInputs.query.all()
    if all_users:
        users_as_json = [user.as_dict() for user in all_users]
        return jsonify(users_as_json)
    else:
        return jsonify([])


@bp.route('/eventinputdropdownkkeys', methods=["GET", "POST"])
def eventinputdropdownkkeys():
    # Query all users
    all_users = EventInputDropdownKeys.query.all()
    if all_users:
        users_as_json = [user.as_dict() for user in all_users]
        return jsonify(users_as_json)
    else:
        return jsonify([])


@bp.route('/delet_event_Inputs_get', methods=["GET", "POST"])
def delet_event_Inputs_get():
    try:
        # Perform deletion query
        db.session.query(EventInputs).delete()
        db.session.commit()
        return 'All records deleted successfully'
    except Exception as e:
        db.session.rollback()
        return f'Error deleting records: {str(e)}'


@bp.route('/user', methods=["GET", "POST"])
@login_required
def user():
    if request.method == "GET":
        user_id_get = session.get('user')
        users = Users.query.filter_by(id=user_id_get).one()
        organization_name_ = users.organization_name
        type_organization_ = users.type_organization
        user_details = Users.query.filter_by(type_organization=users.type_organization,
                                             organization_name=users.organization_name).all()

        first_name_list_ = []
        last_name_list_ = []
        username_list_ = []
        email_id_list_ = []
        department_list_ = []
        role_list_ = []
        id_user__list_ = []
        for user_detail_ in user_details:
            id_user__list_.append(user_detail_.id)
            first_name_list_.append(user_detail_.first_name)
            last_name_list_.append(user_detail_.last_name)
            username_list_.append(user_detail_.username)
            email_id_list_.append(user_detail_.email_id)
            department_list_.append(user_detail_.department)
            role_list_.append(user_detail_.role)
        return render_template('new_user.html', organization_name_=organization_name_,
                               type_organization_=type_organization_, user_details=user_details,
                               id_user__list_=id_user__list_, role_list_=role_list_,
                               first_name_list_=first_name_list_, last_name_list_=last_name_list_,
                               username_list_=username_list_, email_id_list_=email_id_list_,
                               department_list_=department_list_)
    if request.method == "POST":
        user_id_get = session.get('user')
        First_Name = request.form.get('FirstName')
        Last_Name = request.form.get('LastName')
        user_Name = request.form.get('userName')
        password = request.form.get('password')
        mail_id = request.form.get('mail_id')
        org_type = request.form.get('type_organization_')
        org_name = request.form.get('organization_name_')
        department = request.form.get('department')
        role = request.form.get('role')
        head = Users(first_name=First_Name,
                     last_name=Last_Name,
                     username=user_Name,
                     password=password,
                     email_id=mail_id,
                     type_organization=org_type,
                     organization_name=org_name,
                     department=department,
                     role=role,
                     status="A",
                     create_by=user_id_get,
                     access_to_admin="No")
        try:
            db.session.add(head)
            db.session.commit()
            db.session.close()
        except Exception as e:
            LOG.error(e, exc_info=True)
            db.session.rollback()
            LOG.error("Error while pushing data")
            msg = "Failed"
            Status = {"status": msg}

        user_id_get = session.get('user')
        users = Users.query.filter_by(id=user_id_get).one()
        organization_name_ = users.organization_name
        type_organization_ = users.type_organization
        user_details = Users.query.filter_by(type_organization=users.type_organization,
                                             organization_name=users.organization_name).all()
        first_name_list_ = []
        last_name_list_ = []
        username_list_ = []
        email_id_list_ = []
        department_list_ = []
        role_list_ = []
        id_user__list_ = []
        for user_detail_ in user_details:
            id_user__list_.append(user_detail_.id)
            first_name_list_.append(user_detail_.first_name)
            last_name_list_.append(user_detail_.last_name)
            username_list_.append(user_detail_.username)
            email_id_list_.append(user_detail_.email_id)
            department_list_.append(user_detail_.department)
            role_list_.append(user_detail_.role)
        return render_template('new_user.html', organization_name_=organization_name_,
                               type_organization_=type_organization_, user_details=user_details,
                               id_user__list_=id_user__list_, role_list_=role_list_,
                               first_name_list_=first_name_list_, last_name_list_=last_name_list_,
                               username_list_=username_list_, email_id_list_=email_id_list_,
                               department_list_=department_list_)


def convert_date_(date_time_):
    e_start_date = datetime.strptime(date_time_, '%Y-%m-%d')
    final_end_date = e_start_date.strftime("%Y-%m-%d %H:%M:%S.%f")
    Event_Start_Date = datetime.strptime(final_end_date, '%Y-%m-%d %H:%M:%S.%f')
    return Event_Start_Date


def get_organization_name_role_department(organization_name, user_id_get):
    # organization_name = request.form.get('organization_name')
    # users = Users.query.filter(Users.organization_name=organization_name,Users.user_id != user_id_get).all()
    users = Users.query.filter(Users.organization_name == organization_name, Users.id != user_id_get).all()
    unique_keys = set()
    if users:
        for user__ in users:
            role_department = (user__.role, user__.department)
            key = f"{role_department[0]}_{role_department[1]}"
            unique_keys.add(key)
    else:
        unique_keys = []
    return list(unique_keys)


@bp.route('/create_event', methods=["GET", "POST"])
@login_required
def create_event():
    if request.method == "GET":
        user_id_get = session.get('user')
        user_organization_name_get = session.get('event_organizer_id')
        list_unqiue_dep_ = get_organization_name_role_department(user_organization_name_get, user_id_get)
        return render_template('event_creation.html', list_unqiue_dep_=list_unqiue_dep_)
    if request.method == "POST":
        count_of_varables = 0
        user_id_get = session.get('user')
        user_organization_name_get = session.get('event_organizer_id')
        Event_Name = request.form.get('Event_Name')
        Event_Start_Date = convert_date_(request.form.get('Event_Start_Date'))
        Event_End_Date = convert_date_(request.form.get('Event_End_Date'))
        Registration_Start_Date = convert_date_(request.form.get('Registration_Start_Date'))
        Registration_End_Date = convert_date_(request.form.get('Registration_End_Date'))
        event_description = request.form.get('event_description')
        value_for_multiselectds = str(request.form.get('value_for_multiselectd')).split(',')
        g_event_id = datetime.now().strftime("%d%m%Y%H%M%S") + get_random_numbers(5)
        head = Events(event_id=g_event_id, event_name=Event_Name,
                      event_start_date=Event_Start_Date,
                      event_end_date=Event_End_Date,
                      event_registration_start_date=Registration_Start_Date,
                      event_registration_end_date=Registration_End_Date,
                      event_description=event_description,
                      event_organizer_id=user_id_get,
                      event_status='Created')
        try:
            db.session.add(head)
            db.session.commit()
            db.session.close()
        except Exception as e:
            LOG.error(e, exc_info=True)
            db.session.rollback()
            LOG.error("Error while pushing data")
            Status = {"status": "Failed"}
            return jsonify(Status)
        for value_for_multiselectd in value_for_multiselectds:
            temp_valu_ = value_for_multiselectd.split('_')
            if len(temp_valu_) > 1:
                EventsEligibleUsers_ = EventsEligibleUsers(event_id=g_event_id,
                                                           event_organizer_id=user_id_get,
                                                           event_organization_id=user_organization_name_get,
                                                           event_eligible_candidates_role_id=temp_valu_[0],
                                                           event_eligible_candidates_dep_id=temp_valu_[1])
                try:
                    db.session.add(EventsEligibleUsers_)
                    db.session.commit()
                    db.session.close()

                except Exception as e:
                    LOG.error(e, exc_info=True)
                    db.session.rollback()
                    LOG.error("Error while pushing Events Eligible Users_ data")
                    msg = "Failed"
                    Status = {"status": msg}
                    return jsonify(Status)
        return redirect(url_for('view.event_inputs', event_id=g_event_id))


@bp.route('/event_inputs/<string:event_id>', methods=["GET", "POST"])
@login_required
def event_inputs(event_id):
    if request.method == "GET":
        try:
            event_ = Events.query.filter_by(event_id=event_id).one()
            if event_.event_status == 'Created':
                Event_Name = event_.event_name
                Event_Start_Date = event_.event_start_date
                Event_End_Date = event_.event_end_date
                Registration_Start_Date = event_.event_registration_start_date
                Registration_End_Date = event_.event_registration_end_date
                event_description = event_.event_description
                count_of_varables = 0
                return render_template('event_inputs.html', Event_Name=Event_Name,
                                       Event_Start_Date=Event_Start_Date, Event_End_Date=Event_End_Date,
                                       Registration_Start_Date=Registration_Start_Date,
                                       Registration_End_Date=Registration_End_Date,
                                       event_description=event_description, count_of_varables=count_of_varables,
                                       event_id=str(event_id))
            elif event_.event_status == 'In Progress':
                return redirect(url_for("view.manage_event", event_id=event_id))

            else:
                return redirect(url_for("view.create_event"))
        except NoResultFound:
            pass
        except Exception as e:
            LOG.error("Error occurred while searching ")
            LOG.error(e, exc_info=True)
        finally:
            db.session.close()
        return redirect(url_for("view.create_event"))


def clean_list(list_: list):
    temp_list = []
    for ele in list_:
        if bool(str(ele).strip()):
            temp_list.append(str(ele).strip())
    return temp_list


@bp.route('/lbl_creation/<string:event_id>', methods=["GET", "POST"])
@login_required
def create_inputs_for_events(event_id):
    print('event_idinlbl_creation ', event_id)
    data = request.json
    final_list = data[0]["final_list"]
    for i in final_list:
        head = EventInputs(event_id=event_id,
                           label_type=final_list[i]["label_type"],
                           label_name=final_list[i]["label_name"],
                           label_length=final_list[i]["label_length"],
                           label_mandatory=final_list[i]["label_mandatory"])
        try:
            db.session.add(head)
            db.session.commit()
        except Exception as e:
            LOG.error(e, exc_info=True)
            db.session.rollback()
            LOG.error("Error while pushing data")
            msg = "Failed"
            Status = {"status": msg}
            return jsonify(Status)
        if final_list[i]["label_type"] == "DropDown":
            event_inputs_id = head.id
            split_val = str(final_list[i]["label_length"]).split(';')
            split_val = clean_list(split_val)
            if split_val:
                for jj in split_val:
                    head2 = EventInputDropdownKeys(event_id=event_id,
                                                   event_inputs_id=event_inputs_id,
                                                   dropdown_value=str(jj))
                    try:
                        db.session.add(head2)
                        db.session.commit()
                        db.session.close()
                    except Exception as e:
                        LOG.error(e, exc_info=True)
                        db.session.rollback()
                        LOG.error("Error while pushing data")
                        msg = "Failed"
                        Status = {"status": msg}
                        return jsonify(Status)
            else:
                jsonify({'error': "Drop Doesn't contains any value"})

    event_id_get_ = Events.query.filter_by(event_id=event_id).one()
    claims_ = Events(id=event_id_get_.id,
                     event_id=event_id,
                     updated_date=datetime.now(),
                     event_status="In Progress")

    try:
        db.session.merge(claims_)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    db.session.close()
    threading.Thread(target=call_email_function,
                     args=(APP, event_id,)).start()
    return jsonify({'Yo': "Yo Yo"})


def call_email_function(app, event_id):
    try:
        with app.app_context():
            event_id_get_main_ = EventsEligibleUsers.query.filter_by(event_id=event_id).all()
            main_eventd_get_ = Events.query.filter_by(event_id=event_id).one()
            email_id_ = []
            password_ = []
            username_list = []
            candidate_id_for_att = []
            for event_id_get_subn_ in event_id_get_main_:
                event_organizer_id_ = event_id_get_subn_.event_organizer_id
                event_organization_id = event_id_get_subn_.event_organization_id
                event_eligible_candidates_role_id = event_id_get_subn_.event_eligible_candidates_role_id
                event_eligible_candidates_dep_id = event_id_get_subn_.event_eligible_candidates_dep_id
                event_id_get_ = Users.query.filter(Users.role == event_eligible_candidates_role_id,
                                                   Users.department == event_eligible_candidates_dep_id,
                                                   Users.organization_name == event_organization_id,
                                                   Users.id != event_organizer_id_).all()
                for j in event_id_get_:
                    email_id_.append(j.email_id)
                    password_.append(j.password)
                    username_list.append(j.username)
                    candidate_id_for_att.append(j.id)
            event_registartion_start_date = main_eventd_get_.event_registration_start_date
            event_registartion_end_date = main_eventd_get_.event_registration_end_date
            url_ = APP.config["URL_PRO"] + "/userinfoform/" + str(event_id)
            ent_name = main_eventd_get_.event_name

            insert_into_event_att(event_id, candidate_id_for_att, 'Pending')
            send_email_fun(url_, ent_name, "sandeep.kumar.rudhravaram@gmail.com", email_id_, password_, username_list,
                           event_registartion_start_date, event_registartion_end_date, "UNT Event Alert!!!")
            return jsonify({"To": "h"})
    except Exception as e:
        LOG.info(e)
        return jsonify({"To": str(e)})


def insert_into_event_att(event_id, candidate_id, attendance_status):
    print('candidate_idcandidate_id', candidate_id, type(candidate_id))
    if candidate_id:
        if isinstance(candidate_id, list):
            for jj in candidate_id:
                head22 = EventAttendance(event_id=event_id,
                                         candidate_id=jj,
                                         attendance_status=str(attendance_status))
                try:
                    db.session.add(head22)
                    db.session.commit()
                    db.session.close()
                except Exception as e:
                    LOG.error(e, exc_info=True)
                    db.session.rollback()
                    LOG.error("Error while pushing data")
                    msg = "Failed"
                    Status = {"status": msg}
                    return jsonify(Status)
        elif isinstance(candidate_id, str) or isinstance(candidate_id, int):
            print('asadsas')
            head23 = EventAttendance.query.filter_by(event_id=event_id, candidate_id=candidate_id).one()
            head2 = EventAttendance(id=head23.id,
                                    attendance_status=str(attendance_status))
            try:
                db.session.merge(head2)
                db.session.commit()
                db.session.close()
            except Exception as e:
                LOG.error(e, exc_info=True)
                db.session.rollback()
                LOG.error("Error while pushing data")
                msg = "Failed"
                Status = {"status": msg}
                return jsonify(Status)


def get_event_details(event_id):
    Event_Name, Event_Start_Date, Event_End_Date, Registration_Start_Date, Registration_End_Date, event_description, count_of_varables = '', '', '', '', '', '', ''
    try:
        event_ = Events.query.filter_by(event_id=event_id).one()
        Event_Name = event_.event_name
        Event_Start_Date = event_.event_start_date
        Event_End_Date = event_.event_end_date
        Registration_Start_Date = event_.event_registration_start_date
        Registration_End_Date = event_.event_registration_end_date
        event_description = event_.event_description
        count_of_varables = 0
    except NoResultFound:
        pass
    except Exception as e:
        LOG.error("Error occurred while searching ")
        LOG.error(e, exc_info=True)
    finally:
        db.session.close()
    return Event_Name, Event_Start_Date, Event_End_Date, Registration_Start_Date, Registration_End_Date, event_description, count_of_varables


def get_event_inputs_(event_id):
    list_of_label_name = []
    list_of_label_length = []
    list_of_label_mandatory = []
    list_of_label_type = []
    list_of_id = []
    list_int_of_id = []
    dropdown_list_ = {}
    try:
        event_ = EventInputs.query.filter_by(event_id=event_id).all()
        for event_input in event_:
            list_of_label_name.append(event_input.label_name)
            list_of_label_length.append(event_input.label_length)
            list_of_label_mandatory.append(event_input.label_mandatory)
            list_of_label_type.append(event_input.label_type)
            list_of_id.append(str(event_input.id))
            list_int_of_id.append(event_input.id)
            if event_input.label_type == "DropDown":
                eventinputdropdownkeys_ = EventInputDropdownKeys.query.filter_by(event_inputs_id=event_input.id).all()
                lisst_list_of_dks = []
                for eventinputdropdownkey_ in eventinputdropdownkeys_:
                    lisst_list_of_dks.append([eventinputdropdownkey_.dropdown_value, str(eventinputdropdownkey_.id)])
                dropdown_list_[str(event_input.id)] = lisst_list_of_dks

    except NoResultFound:
        pass
    except Exception as e:
        LOG.error("Error occurred while searching ")
        LOG.error(e, exc_info=True)
    finally:
        db.session.close()
    return list_of_label_name, list_of_label_length, list_of_label_mandatory, list_of_label_type, list_of_id, dropdown_list_, list_int_of_id


@bp.route('/userinfoform/<string:event_id>', methods=["GET", "POST"])
@login_required
def get_user_events_info_form(event_id):
    if request.method == "GET":
        access_to_admin_status = session.get('access_to_admin_status')
        if access_to_admin_status == "No":
            access_to_admin_status_hidden = "hidden"
        else:
            access_to_admin_status_hidden = 'unset'
        Event_Name, Event_Start_Date, Event_End_Date, Registration_Start_Date, Registration_End_Date, event_description, count_of_varables = get_event_details(
            event_id)
        user_id_get = session.get('user')
        event_id_get_12 = EventAttendance.query.filter_by(event_id=event_id, candidate_id=user_id_get).one()
        temp_dic_ = {}
        hid_fil_ = ""
        button_dis_ = ""
        txt_disP = r"After selecting 'Create,'you'll be prompted to complete the necessary input fields that users are required to fill."

        registration_start_date_for_check = str(Registration_Start_Date)
        registration_end_date_for_check = str(Registration_End_Date)

        start_date_for_checl = datetime.strptime(registration_start_date_for_check, "%Y-%m-%d %H:%M:%S")
        end_date_for_checl = datetime.strptime(registration_end_date_for_check, "%Y-%m-%d %H:%M:%S")
        current_date_for_checl = datetime.now()

        if event_id_get_12.attendance_status == "Submitted":
            hid_fil_ = "disabled"
            button_dis_ = "none"
            txt_disP = "You already submitted the application"
            event_id_12 = EventInputsInfo.query.filter_by(candidate_id=user_id_get).all()
            for i in event_id_12:
                temp_dic_[i.event_inputs_id] = i.event_inputs_answer
        elif not (start_date_for_checl <= current_date_for_checl):
            hid_fil_ = "disabled"
            button_dis_ = "none"
            txt_disP = "Registration will  start on " + str(start_date_for_checl)
        elif not (current_date_for_checl <= end_date_for_checl):
            hid_fil_ = "disabled"
            button_dis_ = "none"
            txt_disP = "Event Registration  Ended on " + str(end_date_for_checl)

        list_of_label_name, list_of_label_length, list_of_label_mandatory, list_of_label_type, list_of_id, dropdown_list_, list_int_of_id = get_event_inputs_(
            event_id)

        list_of_answers_ = []
        if temp_dic_:
            for i in list_int_of_id:
                list_of_answers_.append(temp_dic_[str(i)])
        print('list_of_answers_', list_of_answers_)
        return render_template('user_events_info_form.html', Event_Name=Event_Name,
                               Event_Start_Date=Event_Start_Date, Event_End_Date=Event_End_Date,
                               Registration_Start_Date=Registration_Start_Date,
                               Registration_End_Date=Registration_End_Date,
                               event_description=event_description, count_of_varables=count_of_varables,
                               event_id=str(event_id), list_of_label_name=list_of_label_name,
                               list_of_label_length=list_of_label_length
                               , list_of_label_mandatory=list_of_label_mandatory,
                               list_of_label_type=list_of_label_type, list_of_id=list_of_id,
                               dropdown_list_=dropdown_list_, list_of_answers_=list_of_answers_, hid_fil_=hid_fil_,
                               button_dis_=button_dis_, txt_disP=txt_disP,
                               access_to_admin_status_hidden=access_to_admin_status_hidden)
    if request.method == "POST":
        user_id_get = session.get('user')
        list_of_label_name, list_of_label_length, list_of_label_mandatory, list_of_label_type, list_of_id, dropdown_list_, list_int_of_id = get_event_inputs_(
            event_id)
        final_dic_ = {}
        for id_ in range(len(list_of_id)):
            if list_of_label_type[id_] == 'Textbook':
                final_dic_[list_int_of_id[id_]] = request.form.get('Textbook_' + str(list_of_id[id_]))
            elif list_of_label_type[id_] == 'DropDown':
                final_dic_[list_int_of_id[id_]] = request.form.get('DropDown_' + str(list_of_id[id_]))
            elif list_of_label_type[id_] == 'Date':
                final_dic_[list_int_of_id[id_]] = convert_date_(request.form.get('Date_fr_' + str(list_of_id[id_])))
            elif list_of_label_type[id_] == 'textarea':
                final_dic_[list_int_of_id[id_]] = request.form.get('textarea_' + str(list_of_id[id_]))
        for data_ in final_dic_:
            try:
                tariff = EventInputsInfo(event_id=event_id,
                                         candidate_id=user_id_get,
                                         event_inputs_id=data_,
                                         event_inputs_answer=final_dic_[data_])
                db.session.add(tariff)
                db.session.commit()
                db.session.close()
            except IndexError:
                break
            except Exception as e:
                LOG.error("Error while pushing bill data data")
                LOG.error(e, exc_info=True)
                db.session.rollback()
        insert_into_event_att(event_id, user_id_get, "Submitted")

        Event_Name, Event_Start_Date, Event_End_Date, Registration_Start_Date, Registration_End_Date, event_description, count_of_varables = get_event_details(
            event_id)
        return redirect(url_for('view.home'))
        # return render_template('user_events_info_form.html', Event_Name=Event_Name,
        #                        Event_Start_Date=Event_Start_Date, Event_End_Date=Event_End_Date,
        #                        Registration_Start_Date=Registration_Start_Date,
        #                        Registration_End_Date=Registration_End_Date,
        #                        event_description=event_description, count_of_varables=count_of_varables,
        #                        event_id=str(event_id), list_of_label_name=list_of_label_name,
        #                        list_of_label_length=list_of_label_length
        #                        , list_of_label_mandatory=list_of_label_mandatory,
        #                        list_of_label_type=list_of_label_type, list_of_id=list_of_id,
        #                        dropdown_list_=dropdown_list_)


@bp.route('/get_user_', methods=["GET", "POST"])
def get_user_():
    # Query all users
    all_users = Users.query.all()
    if all_users:
        users_as_json = [user.as_dict() for user in all_users]
        return jsonify(users_as_json)
    else:
        return jsonify([])


@bp.route('/manage_event/<string:event_id>', methods=["GET", "POST"])
@login_required
def manage_event(event_id):
    if request.method == "GET":
        event_ = Events.query.filter_by(event_id=event_id).one()
        Event_Name = event_.event_name
        Event_Start_Date = event_.event_start_date
        Event_End_Date = event_.event_end_date
        Registration_Start_Date = event_.event_registration_start_date
        Registration_End_Date = event_.event_registration_end_date
        event_description = event_.event_description
        count_of_varables = 0
        list_of_label_name, list_of_label_length, list_of_label_mandatory, list_of_label_type, list_of_id, dropdown_list_, list_int_of_id = get_event_inputs_(
            event_id)

        # all_users = EventAttendance.query.filter_by(event_id=event_id).all()

        event_to_attend = db.session.query(Users, EventAttendance).filter(
            EventAttendance.event_id == event_id).outerjoin(EventAttendance,
                                                            Users.id == EventAttendance.candidate_id,
                                                            isouter=True).all()
        mail_id_for_table = []
        user_name_for_table_ = []
        status_of_process_for_table = []
        list_of_pending_list_emails_ = []
        list_of_pending_list_password_ = []
        list_of_pending_list_username_ = []
        for User, EventA in event_to_attend:
            mail_id_for_table.append(User.email_id)
            user_name_for_table_.append(User.username)
            status_of_process_for_table.append(EventA.attendance_status)
            if EventA.attendance_status == "Pending":
                list_of_pending_list_emails_.append(User.email_id)
                list_of_pending_list_username_.append(User.username)
                list_of_pending_list_password_.append(User.password)
        butn_func_ = ""
        if not list_of_pending_list_emails_:
            butn_func_ = "none"
        # send_email_fun(url_, ent_name, "sandeep.kumar.rudhravaram@gmail.com", email_id_, password_,
        #                username_list,
        #                event_registartion_start_date, event_registartion_end_date)

        return render_template('event_manager.html', Event_Name=Event_Name,
                               Event_Start_Date=Event_Start_Date, Event_End_Date=Event_End_Date,
                               Registration_Start_Date=Registration_Start_Date,
                               Registration_End_Date=Registration_End_Date,
                               event_description=event_description, count_of_varables=count_of_varables,
                               event_id=str(event_id), lisT_for_manage_label_type=list_of_label_type,
                               lisT_for_manage_label_name=list_of_label_name,
                               lisT_for_manage_label_length=list_of_label_length,
                               lisT_for_manage_label_mandatory=list_of_label_mandatory,
                               lisT_for_manage_ids=list_int_of_id,
                               list_of_pending_list_password_=list_of_pending_list_password_,
                               list_of_pending_list_emails_=list_of_pending_list_emails_,
                               list_of_pending_list_username_=list_of_pending_list_username_,
                               mail_id_for_table=mail_id_for_table, user_name_for_table_=user_name_for_table_,
                               status_of_process_for_table=status_of_process_for_table, butn_func_=butn_func_)
        # except NoResultFound:
        #     pass
        # except Exception as e:
        #     LOG.error("Error occurred while searching ")
        #     LOG.error(e, exc_info=True)
        # finally:
        #     db.session.close()
        # return redirect(url_for("view.create_event"))


@bp.route('/delete_event/<string:event_id>', methods=["GET", "POST"])
@login_required
def delete_event(event_id):
    try:
        Events.query.filter_by(event_id=event_id).delete()
        db.session.commit()
    except Exception as e:
        LOG.error("Error while deleting bill entries " + event_id)
        LOG.error(e, exc_info=True)
        pass
    try:
        EventInputs.query.filter_by(event_id=event_id).delete()
        db.session.commit()
    except Exception as e:
        LOG.error("Error while deleting bill entries " + event_id)
        LOG.error(e, exc_info=True)
        pass
    try:
        EventInputsInfo.query.filter_by(event_id=event_id).delete()
        db.session.commit()
    except Exception as e:
        LOG.error("Error while deleting bill entries " + event_id)
        LOG.error(e, exc_info=True)
        pass
    try:
        EventInputDropdownKeys.query.filter_by(event_id=event_id).delete()
        db.session.commit()
    except Exception as e:
        LOG.error("Error while deleting bill entries " + event_id)
        LOG.error(e, exc_info=True)
        pass
    try:
        EventAttendance.query.filter_by(event_id=event_id).delete()
        db.session.commit()
    except Exception as e:
        LOG.error("Error while deleting bill entries " + event_id)
        LOG.error(e, exc_info=True)
        pass
    try:
        EventsEligibleUsers.query.filter_by(event_id=event_id).delete()
        db.session.commit()
    except Exception as e:
        LOG.error("Error while deleting bill entries " + event_id)
        LOG.error(e, exc_info=True)
        pass
    return jsonify({'deleting': "deleting"})


@bp.route('/save_date/<int:event_id>', methods=['POST'])
def save_date(event_id):
    try:
        data = request.get_json()
        updated_end_date = data['updatedEndDate']

        # Check if the event_id exists
        existing_event = Events.query.get(event_id)
        if not existing_event:
            return jsonify({'success': False, 'error': 'Event not found'})

        # Update the end_date for the specified event_id
        existing_event.event_registration_end_date = updated_end_date
        db.session.commit()

        return jsonify({'success': True, 'message': 'Date saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


def send_email_fun(url_, ent_name, from_='', email_id_=None, password_=None, username_list=None,
                   event_registartion_start_date="", event_registartion_end_date="", reason_=""):
    import smtplib
    from email.message import EmailMessage
    import email
    import os
    import random
    import re
    import string
    from datetime import datetime
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    if not email_id_ or not isinstance(email_id_, list):
        raise ValueError("Recipient list is empty or not a list")

    for recipient in range(len(email_id_)):
        msg = EmailMessage()
        msg['Subject'] = reason_ + "  " + ent_name
        msg['From'] = from_
        msg['To'] = email_id_[recipient]
        msg.set_content('This is a plain text email')
        l = f'<!DOCTYPE html> <html lang="en"> <head> <meta charset="utf8"> <meta http-equiv="x-ua-compatible" content="ie=edge"> <meta name="viewport" content="width=device-width,initial-scale=1"> <meta name="x-apple-disable-message-reformatting"> <title>Your reservation is now confirmed</title> <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet"> <!--  <xml>--> <!--    <o:OfficeDocumentSettings>--> <!--      <o:PixelsPerInch>96</o:PixelsPerInch>--> <!--    </o:OfficeDocumentSettings>--> <!--  </xml>--> <style> '
        l += '''table {border-collapse: collapse;} td,th,div,p,a,h1,h2,h3,h4,h5,h6 {font-family: "Segoe UI", sans-serif; mso-line-height-rule: exactly;} </style> <![endif]--> <style>'''
        l += '@media screen { img { max-width: 100%; } td, th { box-sizing: border-box; } u~div .wrapper { min-width: 100vw; } a[x-apple-data-detectors] { color: inherit; text-decoration: none; } .all-font-roboto { font-family: Roboto, -apple-system, "Segoe UI", sans-serif !important; } .all-font-sans { font-family: -apple-system, "Segoe UI", sans-serif !important; } } @media (max-width: 600px) { .sm-inline-block { display: inline-block !important; } .sm-hidden { display: none !important; } .sm-leading-32 { line-height: 32px !important; } .sm-p-20 { padding: 20px !important; } .sm-py-12 { padding-top: 12px !important; padding-bottom: 12px !important; } .sm-text-center { text-align: center !important; } .sm-text-xs { font-size: 12px !important; } .sm-text-lg { font-size: 18px !important; } .sm-w-1-4 { width: 25% !important; } .sm-w-3-4 { width: 75% !important; } .sm-w-full { width: 100% !important; } } </style> <style> @media (max-width: 600px) { .sm-dui17-b-t { border: solid #4299e1; border-width: 4px 0 0; } } </style> <style> .container_forj { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.6rem; } </style> </head>'
        l += f'<body> <div class="container_forj" style="background-color: #f5dbce ;"> <div style="padding: 20px 20px; flex: 1 1 auto; position: relative;"> <div align="left" class="sm-p-20 sm-dui17-b-t" style="border-radius: 10px; padding: 40px; position: relative; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, .1), 0 4px 6px -2px rgba(0, 0, 0, .05); vertical-align: top; z-index: 50;background-color: #ffffff ;margin-right: 200px;margin-left:260px;" valign="top"> <table width="100%" cellpadding="0" cellspacing="0" role="presentation"> <tr> <td width="80%"> <h1 class="sm-text-lg all-font-roboto" style="font-weight: 700; line-height: 100%; margin: 0; margin-bottom: 4px; font-size: 24px;">{ent_name}</h1> <p class="sm-text-xs" style="margin: 0; color: #a0aec0; font-size: 14px;">Event information and details</p> </td> <td style="text-align: right;" width="20%" align="right"> <a href="https://raw.githubusercontent.com/fuelquote/images/23ecd25db8bfe11cb4010e9ee4bf0a6bc53e75d4/petroleum-svgrepo-com.svg" target="_blank" style="text-decoration: none;"> <img src="https://raw.githubusercontent.com/fuelquote/images/main/petroleum-svgrepo-com.png" alt="Download PDF" style="border: 0; line-height: 100%; vertical-align: middle; font-size: 12px;" width="40"> </a> </td> </tr> </table> <div style="line-height: 32px;">&zwnj;</div> <table class="sm-leading-32" style="line-height: 28px; font-size: 14px;" width="100%" cellpadding="0" cellspacing="0" role="presentation"> <tr> <td class="sm-inline-block" style="color: #718096;" width="50%">User Name</td> <td class="sm-inline-block" style="font-weight: 600; text-align: right;" width="50%" align="right">{str(username_list[recipient])}</td> </tr> <tr> <td class="sm-inline-block" style="color: #718096;" width="50%">Password</td> <td class="sm-inline-block" style="font-weight: 600; text-align: right;" width="50%" align="right">{password_[recipient]}</td> </tr> <tr> <td class="sm-w-1-4 sm-inline-block" style="color: #718096;" width="50%">Url</td> <td class="sm-w-3-4 sm-inline-block" style="font-weight: 600; text-align: right;" width="50%" align="right">{str(url_)}</td> </tr> </table> <table width="100%" cellpadding="0" cellspacing="0" role="presentation"> <tr> <td style="padding-top: 24px; padding-bottom: 24px;"> <div style="background-color: #edf2f7; height: 2px; line-height: 2px;">&zwnj;</div> </td> </tr> </table> <table style="font-size: 14px;" width="100%" cellpadding="0" cellspacing="0" role="presentation"> <tr> <td class="sm-w-full sm-inline-block sm-text-center" width="40%"> <p class="all-font-roboto" style="margin: 0; margin-bottom: 4px; color: #a0aec0; font-size: 10px; text-transform: uppercase; letter-spacing: 1px;">Registartion Start Date</p> <p class="all-font-roboto" style="font-weight: 600; margin: 0; color: #000000;">{str(event_registartion_start_date)}</p> </td> <td class="sm-w-full sm-inline-block sm-py-12" style="font-family: Menlo, Consolas, monospace; font-weight: 600; text-align: center; color: #cbd5e0; font-size: 18px; letter-spacing: -1px;" width="20%" align="center">&gt;&gt;&gt;</td> <td class="sm-w-full sm-inline-block sm-text-center" style="text-align: right;" width="40%" align="right"> <p class="all-font-roboto" style="margin: 0; margin-bottom: 4px; color: #a0aec0; font-size: 10px; text-transform: uppercase; letter-spacing: 1px;">Registartion End Date</p> <p class="all-font-roboto" style="font-weight: 600; margin: 0; color: #000000;">{str(event_registartion_end_date)}</p> </td> </tr> </table> <table width="100%" cellpadding="0" cellspacing="0" role="presentation"> <tr> <td style="padding-top: 24px; padding-bottom: 24px;"> <div style="background-color: #edf2f7; height: 2px; line-height: 2px;">&zwnj;</div> <div style="font-weight: 600; padding-top: 32px; text-align: center; color: #000000; font-size: 20px;" width="50%" align="center"">Hurry</div> </td> </tr> </table> <table style="line-height: 28px; font-size: 14px;" width="100%" cellpadding="0" cellspacing="0" role="presentation"> <tr> <td style="color: #718096;" width="50%"></td> <td style="font-weight: 600; text-align: right;" width="50%" align="right"></td> </tr> <tr> <td style="font-weight: 600; padding-top: 32px; color: #000000; font-size: 20px;" width="50%"></td> <td style="font-weight: 600; padding-top: 32px; text-align: right; color: #68d391; font-size: 20px;" width="50%" align="right"></td> </tr> </table> </div> </div> </div> </body> </html>'

        # msg.add_alternative(l, subtype='html')
        # msg.attach(html_part)
        # Rest of your HTML email construction code...

        # with smtplib.SMTP('smtp.office365.com', 587) as smtp:
        #     smtp.starttls()
        #     smtp.login(from_, 'kdstwwwgvcmdulqm')  # Provide your Outlook password here or use a secure method
        #     smtp.send_message(msg)
        msg.add_alternative(l, subtype='html')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(from_, "exjulkvhparxwnna")
            smtp.send_message(msg)


@bp.route('/send_pending_mails', methods=['POST'])
def send_pending_mails():
    data = request.get_json()
    print("data[0]", data[0])
    ent_name = data[0]["Event_Name_"]
    email_id_ = data[0]['list_of_pending_list_emails_']
    password_ = data[0]['list_of_pending_list_password_']
    username_list = data[0]['list_of_pending_list_username_']
    event_id_ = data[0]['event_id_']
    url_ = APP.config["URL_PRO"] + "/userinfoform/" + str(event_id_)
    event_registartion_start_date = data[0]["event_registartion_start_date"]
    event_registartion_end_date = data[0]["event_registartion_end_date"]
    send_email_fun(url_, ent_name, "sandeep.kumar.rudhravaram@gmail.com", email_id_, password_, username_list,
                   event_registartion_start_date, event_registartion_end_date, "UNT Event Reminder Alert!!!")
    return jsonify({"asdv": "mnasbd"})


@bp.route("/logout", methods=['GET','POST'])
def logout():
    import gc
    session.clear()
    gc.collect()
    invalid_msg = "hidden"
    access_name = "hidden"
    access_pass = "hidden"
    return render_template('register_login.html', invalid_msg=invalid_msg
                           , access_name=access_name, access_pass=access_pass)