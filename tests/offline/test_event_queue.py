from unittest import TestCase

from tests.utils import *
from api.event_queue import parse_building_construction_queue


class Test(TestCase):
    def test_parse_buildings_queue(self):
        soup = soup_from_file('./tests/configs/village2_example2_html_dump.txt')
        queue = parse_building_construction_queue(soup, None)

        expected = "[Event(type:BuildingFinished, at:22:50:53 in None)," \
                   " Event(type:BuildingFinished, at:22:54:24 in None)," \
                   " Event(type:BuildingFinished, at:22:58:30 in None)]"

        assert_str(queue, expected)
