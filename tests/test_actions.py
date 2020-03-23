from unittest import TestCase

from api.credentials import init_credentials
from api.arguments import get_parser
from api.account import Account
from api.actions import construct_building, upgrade_building, demolish_building
import api.village_center as center
import time


class Test(TestCase):
    def test_upgrade_building(self):
        args = get_parser().parse_args(args=["--credentials", "./tests/configs/credentials_dynamic_login.json"])
        credentials = init_credentials(args.credentials_file_path)
        own_uid = credentials.get_own_uid()

        account = Account(own_uid)
        account.update_villages(credentials)
        account.villages[0].force_update(credentials)
        assert construct_building(credentials, account.villages[0], 32, center.Buildings.cranny)
        assert upgrade_building(credentials, account.villages[0], 32)
        time.sleep(8)
        demolish_building(credentials, account.villages[0], 32)
        time.sleep(2)
        demolish_building(credentials, account.villages[0], 32)
        time.sleep(1)

        # make sure we leave an empty server
