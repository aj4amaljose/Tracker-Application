"""
Handles UI using Flask Application
"""
import io
from flask import Flask, render_template, request
from tracker.tracker import get_initial_persons, \
    configurations, load_data, constants, session_helper, utils
from sqlalchemy import create_engine


app = Flask(__name__)


@session_helper.create_session(engine=create_engine(configurations.POI_PG_DB_CONNECTION))
def handle_tracker(session, person_id, days):
    """
    Validates and run tracker search for the input

    :param session: Database session
    :param person_id: Social Number of the Individual
    :param days: Days considered for tracking
    """
    error, connected_identities_str, image_data = None, "No connections Found", None
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
                image_data = tracking.get_visualisation()
                connected_nodes = tracking.get_persons_related
                if connected_nodes:
                    connected_identities = {identity.social_no for identity in connected_nodes}
                    connected_identities_str = ','.join(connected_identities)
            else:
                error = constants.MISSING_IDENTITY
    except Exception as e:
        error = e
    finally:
        return error, connected_identities_str, image_data


@app.route("/tracker", methods=["GET", "POST"])
def tracker():
    """
    Finds out Tracking details for  the person and No of days in scope and output the result in an HTML
    """
    days = request.form['number_of_days']
    social_number = request.form['social_security_number']
    error, connected_identities_str, image_data = \
        handle_tracker(person_id=social_number, days=days)
    if error:
        return render_template('exception.html', message=error)
    return render_template('tracker_results.html',
                           image_data=image_data,
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


@session_helper.create_session(engine=create_engine(configurations.POI_PG_DB_CONNECTION))
def handle_import(session, file, table_name):
    """
    Validates and handles database import

    :param file: Selected file from UI
    :param session: Database Session
    :param table_name: Table Name
    """
    error = None
    try:
        if file and file.filename.endswith('.csv'):
            byte_file_obj = io.BytesIO()
            file.save(dst=byte_file_obj)
            file_obj = utils.covert_byte_io_obj_to_string_io_obj(
                byte_obj=byte_file_obj)
            error = load_data.import_csv(file_obj, table_name, session)
        elif file and not file.filename.endswith('.csv'):
            error = constants.WRONG_FILE_FORMAT
        else:
            error = constants.NO_FILES
    except Exception as e:
        error = e
    finally:
        return error


@app.route("/uploader", methods=["GET", "POST"])
def load_files():
    """
    Loads data and renders HTML
    """
    file_str = None
    if request.method == 'POST':
        file = request.files['file']
        table_name = request.form['table']
        file_str = file.filename
        error = handle_import(file=file, table_name=table_name)

        if error:
            if 'invalid keyword argument' in str(error):
                error = constants.WRONG_FILE_HEADERS
            return render_template('exception.html', message=error)

    return render_template('success_update.html', files=file_str)


if __name__ == '__main__':
    app.run(port=int(configurations.POI_APP_PORT), debug=True)
