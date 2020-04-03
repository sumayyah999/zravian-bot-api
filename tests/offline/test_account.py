from unittest import TestCase

from tests.utils import *
from api.account import parse_profile_page


class Test(TestCase):
    def test_account_from_profile_page(self):
        soup = soup_from_file('./tests/configs/profile_example_html_dump.txt')

        user_villages = parse_profile_page(soup)
        assert_str(user_villages, [('Koo-One', 11464), ('Koo-Zero', 2598), ('Koo-Two', 11463)])
