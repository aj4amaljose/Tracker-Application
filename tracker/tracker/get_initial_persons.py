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
    def __init__(self, person_id, no_of_days):
        super(TrackerHelper, self).__init__()
        self.person_id = person_id
        self.no_of_days = no_of_days

    @Handler.property_memorized
    def person_details(self):
        return get_person_details([self.person_id])

    @Handler.property_memorized
    def calculated_date(self):
        today = date.today()
        lower_date = today - timedelta(days=self.no_of_days)
        return lower_date

    @property
    def get_track_details(self):
        return get_track_details(lower_date=self.calculated_date,
                                 person_social_no=self.person_id)

    @Handler.property_memorized
    def get_persons_related(self):
        tracks = self.get_track_details
        results = get_related_persons(tracks=tracks)
        person_social_nos = {
            row.person_social_no for row in results if row.person_social_no != self.person_id}
        persons = get_person_details(person_social_nos=person_social_nos)
        return persons

    def get_visualisation(self):
        create_visualization(self)




