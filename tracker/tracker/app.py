"""
Handles UI using Flask Application
"""
import os
from flask import Flask, render_template, request
from tracker.tracker import get_initial_persons, load_data, constants, session_helper
from sqlalchemy import create_engine


app = Flask(__name__)


@session_helper.create_session(engine=create_engine(os.environ['TRACKER_DB_URL']))
def handle_tracker(session, person_id, days):
    """
    Validates and run tracker search for the input

    :param session: Database session
    :param person_id: Social Number of the Individual
    :param days: Days considered for tracking
    """
    error, connected_identities_str, path = None, "No connections Found", None
    try:
        if not days:
            days = 0
        else:
            days = int(days)

        if not len(person_id):
            error = constants.MISSING_SOCIAL_NO
        else:
            tracking = get_initial_persons.TrackerHelper(person_id=person_id,
                                                         no_of_days=days,
                                                         session=session)
            if tracking.identity_validation:
                path = tracking.get_visualisation()
                connections = tracking.get_persons_related
                if connections:
                    connected_identities = {identity.social_no for identity in connections}
                    connected_identities_str = ','.join(connected_identities)
            else:
                error = constants.MISSING_IDENTITY
    except Exception as e:
        error = e
    finally:
        return error, connected_identities_str, path


@app.route("/tracker", methods=["GET", "POST"])
def tracker():
    """
    Finds out Tracking details for  the person and No of days in scope and output the result in an HTML
    """
    days = request.form['number_of_days']
    social_number = request.form['social_security_number']
    error, connected_identities_str, path = \
        handle_tracker(person_id=social_number, days=days)
    if error:
        return render_template('exception.html', message=error)
    return render_template('tracker_results.html',
                           path=path,
                           connected_identities=connected_identities_str,
                           social_no=social_number)


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Renders Entry HTML
    """
    if request.method == 'POST' and request.form['submit'] == 'Exit':
        return render_template('thanks.html')
    return render_template('index.html')


@app.route("/modeSelection", methods=["GET", "POST"])
def mode_selection():
    """
    Diverts functional HTMLs using mode selection
    """
    mode = request.form['mode']
    if mode == 'load':
        return render_template('load.html')
    else:
        return render_template('tracker.html')


@session_helper.create_session(engine=create_engine(os.environ['TRACKER_DB_URL']))
def handle_import(session, dir_path):
    """
    Validates and handles database import

    :param dir_path: Directory path from UI
    :param session: Database Session
    """
    error, files_str = None, ''
    try:
        if dir_path:
            uploaded_files = load_data.load_files_in_a_folder(dir_path=dir_path, session=session)
            files_str = ','.join(uploaded_files) if uploaded_files else None
        else:
            error = constants.MISSING_DIR
    except Exception as e:
        error = e
    finally:
        return error, files_str


@app.route("/load_files", methods=["GET", "POST"])
def load_files():
    """
    Loads data and renders HTML
    """
    dir_path = request.form['directory_path']
    error, files_str = handle_import(dir_path)
    if error:
        return render_template('exception.html', message=error)
    else:
        return render_template('success_update.html', files=files_str)


if __name__ == '__main__':
    app.run(debug=True)
