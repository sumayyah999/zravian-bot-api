from unittest import TestCase
from bs4 import BeautifulSoup

from api.village import parse_current_vid


class Test(TestCase):
    def test_parse_current_village_vid(self):
        with open('./tests/configs/village1_example2_html_dump.txt', 'r') as content_file:
            content = content_file.read()
            soup = BeautifulSoup(content, 'html.parser')

            vid = parse_current_vid(soup)
            assert vid == 4007
