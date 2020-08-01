"""
Helps to Track other person, may come in contact with interested person
"""
from datetime import date, timedelta
from tracker.tracker.model import get_track_details, get_related_persons, get_person_details
from tracker.tracker.visualise_data import create_visualization


class Handler(object):
    """
    Base Handler for Trackers
    """

    def __init__(self):
        pass

    @staticmethod
    def property_memorized(func):
        """
        Avoids multiple calculation of the property.

        :param func: Function
        :return: Calculated Value or Stored Value
        """

        def inner(self):
            cache_attr = '_attr_cache_{}'.format(func.__name__)
            if hasattr(self, cache_attr):
                return getattr(self, cache_attr)
            else:
                value = func(self)
                setattr(self, cache_attr, value)
                return value

        return property(inner)


class TrackerHelper(Handler):
    """
    Find out Persons who can be in contact with the interested person.
    """

    def __init__(self, person_id, no_of_days, session):
        super(TrackerHelper, self).__init__()
        self.person_id = person_id
        self.no_of_days = no_of_days
        self.session = session

    @property
    def identity_validation(self):
        return all([self.validate_person_details()])

    def validate_person_details(self):
        if self.person_details:
            return True
        else:
            return False

    @Handler.property_memorized
    def person_details(self):
        return get_person_details([self.person_id], session=self.session)

    @Handler.property_memorized
    def calculated_date(self):
        today = date.today()
        lower_date = today - timedelta(days=self.no_of_days)
        return lower_date

    @property
    def get_track_details(self):
        return get_track_details(lower_date=self.calculated_date,
                                 person_social_no=self.person_id,
                                 session=self.session)

    @Handler.property_memorized
    def get_persons_related(self):
        """
        Get persons contact to the person
        :return:
        """
        persons = []
        tracks = self.get_track_details
        if tracks:
            results = get_related_persons(tracks=tracks, session=self.session)
            person_social_nos = {
                row.person_social_no for row in results if row.person_social_no != self.person_id}
            persons = get_person_details(person_social_nos=person_social_nos, session=self.session)
        return persons

    def get_visualisation(self):
        return create_visualization(self)
