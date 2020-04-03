from unittest import TestCase
import time

from tests.utils import *
from api.credentials import init_credentials
from api.event_queue import EventQueue
from api.account import Account
from api.actions import construct_building, upgrade_building, demolish_building, host_celebration, send_resources
from api.assets import Building, Celebration


class TestEventQueue(TestCase):
    # construct cranny, level up cranny, wait for finish events, demolish 2 levels of cranny
    def test_broadcast_finished_events(self):
        credentials = init_credentials('./tests/configs/credentials_dynamic_login.json')

        own_uid = credentials.get_own_uid()
        account = Account(own_uid)
        account.update_villages(credentials)

        village = account.get_village_by_vid(4207)
        village.force_update(credentials)

        assert construct_building(credentials, village, 32, Building.cranny)
        assert upgrade_building(credentials, village, 32)
        b = village.buildings[32]
        assert_str(b, 'Building((Cranny - lvl:0+2 id:32))')

        actions_left = 2
        num_sleep = 0
        while actions_left > 0:
            num = account.events.broadcast_finished_events()
            if num:
                actions_left -= num
                village.force_update(credentials)
                print(b, " event_queue test @ building")
                assert_le(2 - actions_left, b.lvl)

            time.sleep(0.5)
            num_sleep += 1

        assert_lt(num_sleep, 2 * 13.5)
        assert_lt(num_sleep, 2 * 12.5)
        assert_lt(num_sleep, 2 * 11.5)

        demolish_building(credentials, village, 32)
        time.sleep(2)
        demolish_building(credentials, village, 32)
        time.sleep(1)

        village.force_update(credentials)
        assert_str(b, 'Building((Empty place - lvl:0 id:32))')

    # TODO(@alexvelea) merge this with the test above
    def test_demolish_events(self):
        return
        credentials = init_credentials('./tests/configs/credentials_dynamic_login.json')

        own_uid = credentials.get_own_uid()
        account = Account(own_uid)
        account.update_villages(credentials)

        village = account.get_village_by_vid(4007)
        village.force_update(credentials)

        assert construct_building(credentials, village, 25, Building.barracks)
        actions_left = 4
        num_sleep = 0
        while actions_left > 0:
            num = account.events.broadcast_finished_events()
            if num:
                actions_left -= num
                if actions_left % 2 == 1:
                    village.force_update(credentials)
                    demolish_building(credentials, village, 25)
                elif actions_left != 0:
                    village.force_update(credentials)
                    assert construct_building(credentials, village, 25, Building.barracks)

            time.sleep(0.5)
            num_sleep += 1

        assert_lt(num_sleep / 2, 20)

    def test_celebration_events(self):
        credentials = init_credentials('./tests/configs/credentials_dynamic_login.json')

        own_uid = credentials.get_own_uid()
        account = Account(own_uid)
        account.update_villages(credentials)

        village = account.get_village_by_vid(4007)
        village.force_update(credentials)

        host_celebration(credentials, village, Celebration.small)

        evq = account.events
        found = False

        for event in evq.queue:
            if event.event_type == EventQueue.CelebrationCompleted and event.village.vid == village.vid:
                found = True

        assert_eq(found, 1)

    def test_send_resources(self):
        credentials = init_credentials('./tests/configs/credentials_dynamic_login.json')

        own_uid = credentials.get_own_uid()
        account = Account(own_uid)
        account.update_villages(credentials)

        village = account.get_village_by_vid(4007)
        target_village = account.get_village_by_vid(4207)
        village.force_update(credentials)

        send_resources(credentials, village, target_village, [1, 1, 1, 1])

        evq = account.events
        num = 0

        for event in evq.queue:
            if event.event_type == EventQueue.TradersArrived and event.village.vid == village.vid:
                num += 1

        assert_eq(num, 1)
