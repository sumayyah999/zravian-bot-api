from unittest import TestCase
from bs4 import BeautifulSoup

from api.account import parse_profile_page, Account
from api.arguments import get_parser
from api.config import init_config


class Test(TestCase):
    def test_parse_resources(self):
        with open('./tests/configs/profile_example_html_dump.txt', 'r') as content_file:
            content = content_file.read()
            soup = BeautifulSoup(content, 'html.parser')

            user_villages = parse_profile_page(soup)
            user_villages_str = str(user_villages)

            expected = "[('Koo-One', '1168'), ('Koo-Zero', '1051'), ('Koo-Two', '214')]"
            assert user_villages_str == expected


# @TODO(alexvelea): Re-enable the test when there is a static account with the log-in function implemented
class TestAccount(TestCase):
    def test_update_villages(self):
        pass

        # args = get_parser().parse_args(args=["--config", "./tests/configs/config_login_example.json"])
        # config = init_config(args.config_file_path)
        #
        # account = Account(config)
        # user_villages = account.update_villages()
        # user_villages_str = str(user_villages)
        # print(user_villages_str)
        #
        # expected = """[("SwissRhino's village", '290')]"""
        # assert user_villages_str == expected

