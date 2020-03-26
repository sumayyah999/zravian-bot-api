from unittest import TestCase

from api.credentials import init_credentials, BadLogin, BadCookies
from api.arguments import get_parser
from api.account import Account


class Test(TestCase):
    def test_credentials_cookie(self):
        args = get_parser().parse_args(args=["--credentials", "./tests/configs/credentials_static_cookies.json"])
        credentials = init_credentials(args.credentials_file_path)

        assert credentials.url == "https://s3.zravian.com/"

        assert "_ga" in credentials.cookies
        assert "_gid" in credentials.cookies
        assert "PHPSESSID" in credentials.cookies
        assert "lvl" in credentials.cookies
        assert "_gat" in credentials.cookies

    def test_credentials_bad_login(self):
        args = get_parser().parse_args(args=["--credentials", "./tests/configs/credentials_static_login_bad.json"])
        try:
            init_credentials(args.credentials_file_path)
        except BadLogin:
            pass

    def test_credentials_bad_cookies(self):
        args = get_parser().parse_args(args=["--credentials", "./tests/configs/credentials_static_cookies_bad.json"])
        try:
            init_credentials(args.credentials_file_path)
        except BadCookies:
            pass


class TestCredentials(TestCase):
    def test_get_own_uid(self):
        args = get_parser().parse_args(args=["--credentials", "./tests/configs/credentials_static_cookies.json"])
        credentials = init_credentials(args.credentials_file_path)
        own_uid = credentials.get_own_uid()

        account = Account(own_uid)
        account.update_villages(credentials)
        user_villages_str = str(list(map(lambda x: str(x), account.villages)))

        expected = """["api-static's village (20,7)"]"""
        assert user_villages_str == expected
