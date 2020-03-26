from unittest import TestCase
from bs4 import BeautifulSoup

from api.account import parse_profile_page, Account
from api.credentials import init_credentials


class Test(TestCase):
    # Offline version - test from html dump
    def test_account_from_profile_page(self):
        with open('./tests/configs/profile_example_html_dump.txt', 'r') as content_file:
            content = content_file.read()
            soup = BeautifulSoup(content, 'html.parser')

            user_villages = parse_profile_page(soup)
            user_villages_str = str(user_villages)

            expected = "[('Koo-One', 11464), ('Koo-Zero', 2598), ('Koo-Two', 11463)]"
            assert user_villages_str == expected


class TestAccount(TestCase):
    # Online version - request profile of multi hunter
    def test_account_from_profile_page(self):
        credentials = init_credentials('./tests/configs/credentials_static_cookies.json')

        account = Account(uid=1)
        account.update_villages(credentials)
        account.update_villages(credentials)
        user_villages_str = str(list(map(lambda x: str(x), account.villages)))

        expected = "['Multihunter (0,0)']"
        assert user_villages_str == expected
