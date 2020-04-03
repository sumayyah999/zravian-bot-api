from unittest import TestCase

from tests.utils import *
from api.credentials import init_credentials
from api.account import Account


class Test(TestCase):
    def test_parse_buildings(self):
        credentials = init_credentials('../configs/credentials_static_cookies.json')

        own_uid = credentials.get_own_uid()
        account = Account(own_uid)
        account.update_villages(credentials)

        village = account.villages[0]
        village.force_update(credentials)
        expected = "Buildings([Building((Empty place - lvl:0 id:0)), Building((Woodcutter - lvl:0 id:1)), Building((" \
                   "Cropland - lvl:0 id:2)), Building((Woodcutter - lvl:2 id:3)), Building((Iron Mine - lvl:0 id:4)), " \
                   "Building((Clay Pit - lvl:0 id:5)), Building((Clay Pit - lvl:4 id:6)), Building((Iron Mine - lvl:0 " \
                   "id:7)), Building((Cropland - lvl:0 id:8)), Building((Cropland - lvl:0 id:9)), Building((Iron Mine " \
                   "- lvl:0 id:10)), Building((Iron Mine - lvl:0 id:11)), Building((Cropland - lvl:0 id:12)), " \
                   "Building((Cropland - lvl:0 id:13)), Building((Woodcutter - lvl:0 id:14)), Building((Cropland - " \
                   "lvl:3 id:15)), Building((Clay Pit - lvl:0 id:16)), Building((Woodcutter - lvl:0 id:17)), " \
                   "Building((Clay Pit - lvl:0 id:18)), Building((Warehouse - lvl:1 id:19)), Building((Granary - " \
                   "lvl:1 id:20)), Building((Empty place - lvl:0 id:21)), Building((Empty place - lvl:0 id:22)), " \
                   "Building((Empty place - lvl:0 id:23)), Building((Empty place - lvl:0 id:24)), Building((Empty " \
                   "place - lvl:0 id:25)), Building((Main Building - lvl:3 id:26)), Building((Empty place - lvl:0 " \
                   "id:27)), Building((Empty place - lvl:0 id:28)), Building((Empty place - lvl:0 id:29)), " \
                   "Building((Empty place - lvl:0 id:30)), Building((Empty place - lvl:0 id:31)), Building((Empty " \
                   "place - lvl:0 id:32)), Building((Empty place - lvl:0 id:33)), Building((Empty place - lvl:0 " \
                   "id:34)), Building((Empty place - lvl:0 id:35)), Building((Empty place - lvl:0 id:36)), " \
                   "Building((Empty place - lvl:0 id:37)), Building((Empty place - lvl:0 id:38)), Building((Rally " \
                   "Point - lvl:0 id:39)), Building((Empty place - lvl:0 id:0))]) "

        assert_str(village.buildings, expected)
