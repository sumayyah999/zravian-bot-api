from unittest import TestCase
from bs4 import BeautifulSoup
import time

from api.arguments import get_parser
from api.credentials import init_credentials
from api.event_queue import parse_buildings_queue
from api.account import Account
from api.actions import construct_building, upgrade_building, demolish_building
import api.village_center as center


class TestEventQueue(TestCase):
    def test_broadcast_finished_events(self):
        args = get_parser().parse_args(args=["--credentials", "./tests/configs/credentials_dynamic_login.json"])
        credentials = init_credentials(args.credentials_file_path)
        own_uid = credentials.get_own_uid()

        account = Account(own_uid)
        account.update_villages(credentials)

        village = account.get_village_by_vid(4207)
        village.force_update(credentials)

        assert construct_building(credentials, village, 32, center.Buildings.cranny)
        assert upgrade_building(credentials, village, 32)

        actions_left = 2
        num_sleep = 0
        while actions_left > 0:
            actions_left -= account.events.broadcast_finished_events()
            time.sleep(0.5)
            num_sleep += 1

        assert num_sleep < 2 * 13.5
        assert num_sleep < 2 * 12.5
        assert num_sleep < 2 * 11.5

        demolish_building(credentials, village, 32)
        time.sleep(2)
        demolish_building(credentials, village, 32)
        time.sleep(1)


class Test(TestCase):
    def test_parse_buildings_queue(self):
        with open('./tests/configs/village2_example2_html_dump.txt', 'r') as content_file:
            content = content_file.read()
            soup = BeautifulSoup(content, 'html.parser')

            queue = parse_buildings_queue(soup, None)
            queue_str = str(list(map(lambda x: str(x), queue)))

            expected = "['BuildingFinished at 22:50:53 in None',"\
                       " 'BuildingFinished at 22:54:24 in None',"\
                       " 'BuildingFinished at 22:58:30 in None']"

            assert queue_str == expected
