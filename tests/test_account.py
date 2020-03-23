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

            expected = "[('Koo-One', 11464), ('Koo-Zero', 2598), ('Koo-Two', 11463)]"
            assert user_villages_str == expected


class TestAccount(TestCase):
    def test_update_villages(self):
        args = get_parser().parse_args(args=["--credentials", "./tests/configs/credentials_login_example.json"])
        credentials = init_credentials(args.credentials_file_path)

        account = Account(uid=1)
        account.update_villages(credentials)
        account.update_villages(credentials)
        user_villages_str = str(list(map(lambda x: str(x), account.villages)))

        expected = "['Multihunter (0,0)']"
        assert user_villages_str == expected
