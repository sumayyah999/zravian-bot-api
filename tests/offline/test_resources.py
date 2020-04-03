from unittest import TestCase

from tests.utils import *
from api.resources import parse_own


class Test(TestCase):
    def test_parse_resources(self):
        soup = soup_from_file('./tests/configs/village1_example_html_dump.txt')
        village_res = parse_own(soup)

        expected = "VilResources(prod:[27264, 35072, 28416, 26748], stored:[107389, 107436, 115071, 101464], capacity:[128000, 128000, 128000, 108800])"
        assert_str(village_res, expected)
