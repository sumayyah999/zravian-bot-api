from unittest import TestCase
from bs4 import BeautifulSoup

from api.resources import parse_resources


class Test(TestCase):
    def test_parse_resources(self):
        with open('./configs/village1-example.html', 'r') as content_file:
            content = content_file.read()
            soup = BeautifulSoup(content, 'html.parser')

            village_res = parse_resources(soup)
            village_res_str = str(village_res)

            expected = """Woodcutter	2 @ 1
Cropland	10 @ 2
Woodcutter	10 @ 3
Iron Mine	0 @ 4
Clay Pit	7 @ 5
Clay Pit	10 @ 6
Iron Mine	10 @ 7
Cropland	0 @ 8
Cropland	0 @ 9
Iron Mine	3 @ 10
Iron Mine	1 @ 11
Cropland	0 @ 12
Cropland	0 @ 13
Woodcutter	0 @ 14
Cropland	0 @ 15
Clay Pit	0 @ 16
Woodcutter	0 @ 17
Clay Pit	0 @ 18
production: [27264, 35072, 28416, 26748]
stored: [107389, 107436, 115071, 101464]
capacity: [128000, 128000, 128000, 108800]
wheat_consumption: 132
"""

            assert village_res_str == expected
