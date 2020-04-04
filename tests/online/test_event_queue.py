from unittest import TestCase
import time

from tests.utils import *
from api.credentials import init_credentials
from api.event_queue import EventQueue
from api.account import Account
from api.actions import construct_building, upgrade_building, demolish_building, host_celebration, send_resources
from api.assets import Building, Celebration


class TestEventQueue(TestCase):
    # Construct cranny, Lvl up cranny, demolish 2 levels, construct cranny, demolish cranny
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

        actions_left = 6
        num_times_sleep = 0
        time_granularity = 0.1
        while actions_left > 0:
            num = account.events.broadcast_finished_events()
            if num:
                assert_eq(num, 1)
                actions_left -= 1
                village.force_update(credentials)

                if actions_left == 5:
                    assert_str(b, 'Building((Cranny - lvl:1+1 id:32))')
                if actions_left == 4:
                    assert_str(b, 'Building((Cranny - lvl:2 id:32))')
                    demolish_building(credentials, village, 32)
                if actions_left == 3:
                    assert_str(b, 'Building((Cranny - lvl:1 id:32))')
                    demolish_building(credentials, village, 32)
                if actions_left == 2:
                    assert_str(b, 'Building((Empty place - lvl:0 id:32))')
                    assert construct_building(credentials, village, 32, Building.cranny)
                if actions_left == 1:
                    assert_str(b, 'Building((Cranny - lvl:1 id:32))')
                    demolish_building(credentials, village, 32)
                if actions_left == 0:
                    assert_str(b, 'Building((Empty place - lvl:0 id:32))')

            time.sleep(time_granularity)
            num_times_sleep += 1

        # Assert time to complete, for a relative benchmark
        assert_lt(num_times_sleep * time_granularity, 18.0)

    # Host a celebration and check if 
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
