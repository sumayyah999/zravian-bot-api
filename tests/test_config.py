from unittest import TestCase

from api.config import init_config
from api.arguments import get_parser


class Test(TestCase):
    def test_config_cookie(self):
        args = get_parser().parse_args(args=["--config", "./tests/configs/config_cookie_example.json"])
        config = init_config(args.config_file_path)

        assert config.url == "https://s3.zravian.com/"

        assert "_ga" in config.cookies
        assert "_gid" in config.cookies
        assert "PHPSESSID" in config.cookies
        assert "lvl" in config.cookies
        assert "_gat" in config.cookies

    def test_config_login(self):
        args = get_parser().parse_args(args=["--config", "./tests/configs/config_login_example.json"])
        config = init_config(args.config_file_path)

        assert config.url == "https://s3.zravian.com/"

    def test_config_bad_login(self):
        args = get_parser().parse_args(args=["--config", "./tests/configs/config_bad_login_example.json"])
        config = init_config(args.config_file_path)

        assert config is None
