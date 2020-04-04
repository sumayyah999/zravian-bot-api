from unittest import TestCase

from tests.utils import *
from api.buildings import BuildingInstance, Building
from api.account import Account
from api.village import Village
from api.credentials import Page


class Test(TestCase):
    def test_building_type_ordering(self):
        buildings = [
            BuildingInstance(Building.mainB, lvl=5, plus_lvl=3, location_id=0),
            BuildingInstance(Building.granary, lvl=3, plus_lvl=4, location_id=0),
            BuildingInstance(Building.warehouse, lvl=7, plus_lvl=0, location_id=0),
            BuildingInstance(Building.barracks, lvl=6, plus_lvl=0, location_id=0),
        ]

        a = buildings[0]
        b = buildings[1]
        c = buildings[2]

        assert b == c
        assert b >= c
        assert c >= b
        assert b < a
        assert a > b
        assert c <= a
        assert a != b

        assert_eq(max(buildings).lvl, 5)
        assert_eq(min(buildings).lvl, 6)

    def test_parse_buildings(self):
        account = get_dumped_account()
        village = account.villages[0]

        expected = "Buildings([Building((Empty place - lvl:0 id:0)), Building((Woodcutter - lvl:16 id:1)), Building((" \
                   "Cropland - lvl:18 id:2)), Building((Woodcutter - lvl:16 id:3)), Building((Iron Mine - lvl:12 " \
                   "id:4)), Building((Clay Pit - lvl:14 id:5)), Building((Clay Pit - lvl:14 id:6)), Building((Iron " \
                   "Mine - lvl:12 id:7)), Building((Cropland - lvl:11 id:8)), Building((Cropland - lvl:19 id:9)), " \
                   "Building((Iron Mine - lvl:13 id:10)), Building((Iron Mine - lvl:12 id:11)), Building((Cropland - " \
                   "lvl:11+1 id:12)), Building((Cropland - lvl:12 id:13)), Building((Woodcutter - lvl:16 id:14)), " \
                   "Building((Cropland - lvl:18 id:15)), Building((Clay Pit - lvl:14 id:16)), Building((Woodcutter - " \
                   "lvl:16 id:17)), Building((Clay Pit - lvl:14 id:18)), Building((Warehouse - lvl:20 id:19)), " \
                   "Building((Granary - lvl:20 id:20)), Building((Warehouse - lvl:20 id:21)), Building((Hero's " \
                   "Mansion - lvl:15 id:22)), Building((Stable - lvl:20 id:23)), Building((Warehouse - lvl:20 " \
                   "id:24)), Building((Marketplace - lvl:3+2 id:25)), Building((Main Building - lvl:20 id:26)), " \
                   "Building((Academy - lvl:19 id:27)), Building((Residence - lvl:20 id:28)), Building((Tournament " \
                   "Square - lvl:20 id:29)), Building((Horse Drinking Pool - lvl:20 id:30)), Building((Granary - " \
                   "lvl:20 id:31)), Building((Town Hall - lvl:10 id:32)), Building((Brickworks - lvl:5 id:33)), " \
                   "Building((Siege Workshop - lvl:20 id:34)), Building((Sawmill - lvl:5 id:35)), Building((Flour " \
                   "Mill - lvl:5 id:36)), Building((Iron Foundry - lvl:0+1 id:37)), Building((Bakery - lvl:5 id:38)), " \
                   "Building((Rally Point - lvl:20 id:39)), Building((Empty place - lvl:0 id:0))])"

        assert_str(village.buildings, expected)
