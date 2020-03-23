from unittest import TestCase

from api.credentials import init_credentials
from api.arguments import get_parser
from api.account import Account
from api.actions import upgrade_building, demolish_building
import time


class Test(TestCase):
    def test_upgrade_building(self):
        args = get_parser().parse_args(args=["--credentials", "./tests/configs/credentials_dynamic_login.json"])
        credentials = init_credentials(args.credentials_file_path)
        own_uid = credentials.get_own_uid()

        account = Account(own_uid)
        account.update_villages(credentials)
        account.villages[0].force_update(credentials)
        ok = upgrade_building(credentials, account.villages[0], 32)
        time.sleep(5)
        demolish_building(credentials, account.villages[0], 32)
        assert ok
