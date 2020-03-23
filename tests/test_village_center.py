from unittest import TestCase
from bs4 import BeautifulSoup

from api.village_center import parse_center


class Test(TestCase):
    def test_parse_resources(self):
        with open('./tests/configs/village2_example_html_dump.txt', 'r') as content_file:
            content = content_file.read()
            soup = BeautifulSoup(content, 'html.parser')

            village_center = parse_center(soup)
            village_center_str = str(village_center)

            expected = """Warehouse	10 @ 19
Granary	2 @ 20
Empty place	0 @ 21
Barracks	4+1 @ 22
Stable	20 @ 23
Empty place	0 @ 24
Empty place	0 @ 25
Main Building	20 @ 26
Academy	5 @ 27
Empty place	0 @ 28
Empty place	0 @ 29
Empty place	0 @ 30
Blacksmith	3 @ 31
Empty place	0 @ 32
Empty place	0 @ 33
Empty place	0 @ 34
Empty place	0 @ 35
Empty place	0 @ 36
Rally Point	1 @ 39
"""

            assert village_center_str == expected
