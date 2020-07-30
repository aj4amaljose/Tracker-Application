"""
Handles db utilities
"""
import os
from sqlalchemy import create_engine, Column, String, Integer, VARCHAR, Date, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, query


engine = create_engine(os.environ['TRACKER_DB_URL'])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class TemplateTable(object):
    """
    Base Template for the Table
    """
    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String)


class Identity(TemplateTable, Base):
    """
    Stores Identity of all Persons
    """
    __tablename__ = "identity"
    social_no = Column(String)


class Location(TemplateTable, Base):
    """
    Stores Location details
    """
    __tablename__ = "location"
    loc_id = Column(String)


class TrackerData(Base):
    """
    Details of locations and people where tracking is enabled
    """
    __tablename__ = "tracker_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    loc_id = Column(VARCHAR)
    person_social_no = Column(VARCHAR)
    date = Column(Date)


def get_track_details(person_social_no, lower_date):
    """
    Get Track details of person for a unique social no and date range

    :param person_social_no: Unique Social No
    :param lower_date: Lower Date Range
    :return: Tracking details of the person for given range of Dates
    """
    values = query.Query([TrackerData], session=session).filter(
        TrackerData.person_social_no == person_social_no).filter(
        TrackerData.date >= lower_date).all()
    return values


def get_person_details(person_social_nos):
    """
    Get Person details from the Identity Table

    :param person_social_nos: Social Numbers whose details are required
    :return: Identity Details
    """
    persons = query.Query([Identity], session=session).filter(
        Identity.social_no.in_(person_social_nos)).all()
    return persons


def get_location_details(loc_ids):
    """
    Get Location Details

    :param loc_ids: location ids
    :return: Location Details
    """
    locations = query.Query([Location], session=session).filter(
        Location.loc_id.in_(loc_ids)).all()
    return locations


def get_related_persons(tracks):
    """
    Find outs other individuals who had come to the location on the same day interested individual visited
    :param tracks: Individual track details for the selected days
    :return:
    """
    query = session.query(TrackerData)
    ands = []
    for track in tracks:
        ands.append(
            and_(
                TrackerData.loc_id == track.loc_id,
                TrackerData.date == track.date,
            )
        )
    query = query.filter(or_(*ands))
    results = query.all()
    return results


def drop_all_tables():
    """
    Deletes all Tables in the mentioned Schema
    """
    Base.metadata.drop_all(bind=engine)


def create_all_tables():
    """
    Creates db if not created
    :return:
    """
    Base.metadata.create_all(bind=engine)


def insert_data(new_rows):
    """
    Updates rows according to the
    :param new_rows: New Table rows
    """
    session.bulk_save_objects(new_rows)
    session.commit()

