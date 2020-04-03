from unittest import TestCase

from tests.utils import *
from api.account import Account
from api.credentials import init_credentials


class TestAccount(TestCase):
    def test_account_from_profile_page(self):
        credentials = init_credentials('./tests/configs/credentials_static_cookies.json')

        # Get Multi hunter account
        account = Account(uid=1)

        # Test double update
        account.update_villages(credentials)
        account.update_villages(credentials)

        assert_str(account.villages, "['Multihunter (0,0)']")
