"""
Helps to load Mandatory Data to track a Person
"""
import csv
from os import listdir, path
from datetime import datetime
from tracker.tracker import model

FILE_MAPPING = {
    'identity': model.Identity,
    'location': model.Location,
    'tracker': model.TrackerData
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
    reader = csv.DictReader(csv_file_path)
    import_rows = []
    for row in reader:
        cleanse_data(row_data=row)
        import_rows.append(metadata(**row))
    return import_rows


def import_csv(file_data, table_name, session):
    """
    Import CSV to the mapped tables

    :param file_data: Im memory file data
    :param table_name: Name of the table
    :param session: Database Session
    :return error: execution error
    """
    error = None
    try:
        for key in FILE_MAPPING.keys():
            if key in table_name:
                metadata = FILE_MAPPING.get(key)
                if metadata:
                    import_rows = read_file(file_data, metadata)
                    model.insert_data(import_rows, session=session)
    except Exception as e:
        error = e
    finally:
        return error
