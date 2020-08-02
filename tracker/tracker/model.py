"""
Handles db utilities
"""

from sqlalchemy import Column, String, Integer, VARCHAR, Date, and_, or_
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


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


def get_track_details(person_social_no, lower_date, session):
    """
    Get Track details of person for a unique social no and date range

    :param person_social_no: Unique Social No
    :param lower_date: Lower Date Range
    :param session: Database session
    :return: Tracking details of the person for given range of Dates
    """
    values = session.query(TrackerData).filter(
        TrackerData.person_social_no == person_social_no).filter(
        TrackerData.date >= lower_date).all()
    return values


def get_person_details(person_social_nos, session):
    """
    Get Person details from the Identity Table

    :param person_social_nos: Social Numbers whose details are required
    :param session: Database session
    :return: Identity Details
    """
    persons = session.query(Identity).filter(
        Identity.social_no.in_(person_social_nos)).all()
    return persons


def get_location_details(loc_ids, session):
    """
    Get Location Details

    :param loc_ids: location ids
    :param session: Database session
    :return: Location Details
    """
    locations = session.query(Location).filter(
        Location.loc_id.in_(loc_ids)).all()
    return locations


def get_related_persons(tracks, session):
    """
    Find outs other individuals who had come to the location on the same day interested individual visited

    :param tracks: Individual track details for the selected days
    :param session: Database session
    :return: Contacts found at the same location of the person of interest for a given time frame
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


def insert_data(new_rows, session):
    """
    Insert rows into the table

    :param new_rows: New Table rows
    :param session: Database session
    """
    session.bulk_save_objects(new_rows)
    session.commit()


