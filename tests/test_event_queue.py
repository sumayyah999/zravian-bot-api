from unittest import TestCase
from bs4 import BeautifulSoup
import time

from api.arguments import get_parser
from api.credentials import init_credentials
from api.event_queue import parse_building_construction_queue
from api.account import Account
from api.actions import construct_building, upgrade_building, demolish_building
from api.assets import Building


class TestEventQueue(TestCase):
    # Online version - construct cranny, level up cranny, wait for finish events, demolish 2 levels of cranny
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
        assert b.name == Building.cranny.name
        assert b.lvl == 0
        assert b.plus_lvl == 2

        actions_left = 2
        num_sleep = 0
        while actions_left > 0:
            num = account.events.broadcast_finished_events()
            if num:
                actions_left -= num
                village.force_update(credentials)
                print(b, " event_queue test @ building")
                assert b.lvl >= 2 - actions_left

            time.sleep(0.5)
            num_sleep += 1

        assert num_sleep < 2 * 13.5
        assert num_sleep < 2 * 12.5
        assert num_sleep < 2 * 11.5

        demolish_building(credentials, village, 32)
        time.sleep(2)
        demolish_building(credentials, village, 32)
        time.sleep(1)

        village.force_update(credentials)
        assert b.name == Building.empty.name
        assert b.lvl == 0
        assert b.plus_lvl == 0

    def test_demolish_events(self):
        credentials = init_credentials('./configs/credentials_dynamic_login.json')

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

        assert num_sleep / 2 < 20


class Test(TestCase):
    # Offline version - parse building construction queue from html dump
    def test_parse_buildings_queue(self):
        with open('./tests/configs/village2_example2_html_dump.txt', 'r') as content_file:
            content = content_file.read()
            soup = BeautifulSoup(content, 'html.parser')

            queue = parse_building_construction_queue(soup, None)
            queue_str = str(list(map(lambda x: str(x), queue)))

            expected = "['BuildingFinished at 22:50:53 in None',"\
                       " 'BuildingFinished at 22:54:24 in None',"\
                       " 'BuildingFinished at 22:58:30 in None']"

            assert queue_str == expected
