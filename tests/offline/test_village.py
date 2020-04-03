from unittest import TestCase

from tests.utils import *
from api.village import parse_current_vid


class Test(TestCase):
    def test_parse_current_village_vid(self):
        soup = soup_from_file('./tests/configs/village1_example2_html_dump.txt')
        vid = parse_current_vid(soup)

        assert_eq(vid, 4007)
