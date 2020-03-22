from unittest import TestCase

from api.credentials import init_credentials
from api.arguments import get_parser


class Test(TestCase):
    def test_credentials_cookie(self):
        args = get_parser().parse_args(args=["--credentials", "./tests/configs/credentials_cookie_example.json"])
        credentials = init_credentials(args.credentials_file_path)

        assert credentials.url == "https://s3.zravian.com/"

        assert "_ga" in credentials.cookies
        assert "_gid" in credentials.cookies
        assert "PHPSESSID" in credentials.cookies
        assert "lvl" in credentials.cookies
        assert "_gat" in credentials.cookies

    def test_credentials_login(self):
        args = get_parser().parse_args(args=["--credentials", "./tests/configs/credentials_login_example.json"])
        credentials = init_credentials(args.credentials_file_path)

        assert credentials.url == "https://s3.zravian.com/"

    def test_credentials_bad_login(self):
        args = get_parser().parse_args(args=["--credentials", "./tests/configs/credentials_bad_login_example.json"])
        credentials = init_credentials(args.credentials_file_path)

        assert credentials is None
