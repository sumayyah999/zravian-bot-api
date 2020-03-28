from unittest import TestCase

from api.credentials import init_credentials
from api.village import Village
from api.account import Account
import api.actions as actions
from api.assets import Unit


class Test(TestCase):
    def test_move_units(self):
        credentials = init_credentials('./configs/credentials_dynamic_login.json')

        own_uid = credentials.get_own_uid()
        account = Account(own_uid)
        account.update_villages(credentials)

        village = account.get_village_by_vid(4007)
        village.force_update(credentials)

        target_village = Village(account=None, vid=3609, name="")

        actions.move_units(credentials, Unit.raid, village, target_village, units={Unit.imperatoris: 1000})

    def test_train(self):
        credentials = init_credentials('./configs/credentials_dynamic_login.json')

        own_uid = credentials.get_own_uid()
        account = Account(own_uid)
        account.update_villages(credentials)

        village = account.get_village_by_vid(4007)
        village.force_update(credentials)

        try:
            actions.train(credentials, village,
                          units={Unit.imperian: 4})

            assert False
        except actions.ActionException as e:
            assert(str(e) == "Required building Barracks for training ['Imperian']")

        actions.train(credentials, village,
                      units={Unit.legati: 4, Unit.imperatoris: 5, Unit.caesaris: 6,
                             Unit.roman_ram: 7})
