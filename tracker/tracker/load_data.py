"""
Helps to load Mandatory Data to track a Person
"""
import csv
from os import listdir, path
from datetime import datetime
from tracker.tracker import model

FILE_MAPPING = {
    'identity_data': model.Identity,
    'location_data': model.Location,
    'tracker_data': model.TrackerData
}


def cleanse_data(row_data):
    """
    Cleans or Format Data that is present in the input

    :param row_data: row data
    """
    try:
        if 'date' in row_data.keys():
            row_data['date'] = datetime.strptime(row_data['date'], '%d/%m/%Y')
    except Exception as exc:
        print(exc)


def read_file(csv_file_path, metadata):
    """
    Read file and generate rows to be imported

    :param csv_file_path: Full file path of the CSV
    :param metadata: Table metadata
    :return: Rows to be imported
    """
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        import_rows = []
        for row in reader:
            cleanse_data(row_data=row)
            import_rows.append(metadata(**row))
    return import_rows


def import_csv(csv_path, session):
    """
    Import CSV to the mapped tables

    :param csv_path: File path of the csv
    :param session: Database Session
    """
    load = False
    try:
        for key in FILE_MAPPING.keys():
            if key in csv_path:
                metadata = FILE_MAPPING.get(key)
                if metadata:
                    import_rows = read_file(csv_path, metadata)
                    model.insert_data(import_rows, session=session)
                    load = True
    except Exception as e:
        load = False
        print(e)
    finally:
        return load


def load_files_in_a_folder(dir_path, session):
    """
    Load files in a folder to db

    :param dir_path: Directory full path
    :param session: Database session
    """
    files = [path.join(dir_path, f) for f in listdir(dir_path) if path.isfile(path.join(dir_path, f))
             and f.endswith('.csv')]
    loaded_files = []
    for file in files:
        status = import_csv(csv_path=file, session=session)
        if status:
            file_name = path.basename(file)
            loaded_files.append(file_name)
    return loaded_files

