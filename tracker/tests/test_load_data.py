"""
Tests module load_data
"""
import pytest
from datetime import datetime
from tracker.tracker import load_data


class MockIdentity(object):
    def __init__(self, social_no, address):
        self.social_no = social_no
        self.address = address


class MockTrackData(object):
    def __init__(self, loc_id, person_social_no, date):
        self.person_social_no = person_social_no
        self.date = date
        self.loc_id = loc_id


@pytest.mark.parametrize("test_input, expected",
                         [({'date': '12/06/2020'}, ('date', datetime)), ({'test': '1'}, ('test', str))])
def test_cleanse_data(test_input, expected):
    load_data.cleanse_data(test_input)
    assert isinstance(test_input[expected[0]], expected[1])
