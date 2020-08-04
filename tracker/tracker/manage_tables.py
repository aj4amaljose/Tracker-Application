"""
Module to create or delete the table
"""
import argparse
from sqlalchemy import create_engine
from tracker.tracker import configurations, model

engine_model_mappings = {
    'tracker_data': [configurations.POI_PG_DB_CONNECTION, model]
}


def manage_all_tables(action, db_engine, db_model):
    """
    Deletes or Creates db if not created

    :param action: action to be performed
    :param db_engine: DB engine
    :param db_model: DB schema model
    """

    base = db_model.Base
    if action == 'create':
        base.metadata.create_all(bind=db_engine)
    else:
        base.metadata.drop_all(bind=db_engine)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='manage app tables')
    choices = ['create', 'delete']
    parser.add_argument('-a', '--action', dest='action', choices=choices,
                        help='Manges tables required for the app, choices are create or action',
                        required=True)
    args = parser.parse_args()
    for schema in engine_model_mappings.keys():
        db_url = engine_model_mappings[schema][0]
        model = engine_model_mappings[schema][1]
        engine = create_engine(configurations.POI_PG_DB_CONNECTION)
        manage_all_tables(action=args.action, db_engine=engine, db_model=model)
        engine.dispose()