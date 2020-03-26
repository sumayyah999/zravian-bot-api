from unittest import TestCase
from bs4 import BeautifulSoup

from api.resources import parse_own


class Test(TestCase):
    # Offline version
    def test_parse_resources(self):
        with open('./tests/configs/village1_example_html_dump.txt', 'r') as content_file:
            content = content_file.read()
            soup = BeautifulSoup(content, 'html.parser')

            village_res = parse_own(soup)
            village_res_str = str(village_res)

            expected = """\
production: [27264, 35072, 28416, 26748]
stored: [107389, 107436, 115071, 101464]
capacity: [128000, 128000, 128000, 108800]
"""

            assert village_res_str == expected
