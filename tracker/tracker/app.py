from flask import Flask, render_template, request
from tracker.tracker import get_initial_persons, load_data

app = Flask(__name__)


@app.route("/tracker", methods=["GET", "POST"])
def need_input():
    days = request.form['number_of_days']
    tracking = get_initial_persons.TrackerHelper(person_id=request.form['social_security_number'],
                                                 no_of_days=int(days) or 0)
    values = tracking.get_persons_related
    ids = {value.social_no for value in values}
    return render_template('tracker_results.html', name=','.join(ids))


@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')


@app.route("/modeSelection", methods=["GET", "POST"])
def mode_selection():
    mode = request.form['mode']
    if mode == 'load':
        return render_template('load.html')
    else:
        return render_template('tracker.html')


@app.route("/load_files", methods=["GET", "POST"])
def load():
    dir_path = request.form['directory_path']
    upload_files = load_data.load_files_in_a_folder(dir_path=dir_path)
    return render_template('success_update.html', files=','.join(upload_files))


if __name__ == '__main__':
    app.run(debug=True)
