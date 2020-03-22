from unittest import TestCase
from bs4 import BeautifulSoup

from api.account import parse_profile_page, Account
from api.arguments import get_parser
from api.credentials import init_credentials


class Test(TestCase):
    def test_parse_resources(self):
        with open('./tests/configs/profile_example_html_dump.txt', 'r') as content_file:
            content = content_file.read()
            soup = BeautifulSoup(content, 'html.parser')

            user_villages = parse_profile_page(soup)
            user_villages_str = str(user_villages)

            expected = "[('Koo-One', '1168'), ('Koo-Zero', '1051'), ('Koo-Two', '214')]"
            assert user_villages_str == expected


class TestAccount(TestCase):
    def test_update_villages(self):
        args = get_parser().parse_args(args=["--credentials", "./tests/configs/credentials_login_example.json"])
        credentials = init_credentials(args.credentials_file_path)

        account = Account(uid=1)
        user_villages = account.update_villages(credentials)
        user_villages_str = str(user_villages)

        expected = "[('Multihunter', '2')]"
        assert user_villages_str == expected

