from unittest import TestCase

from api.credentials import init_credentials
from api.account import Account
from api.buildings import BuildingInstance, Building


class Test(TestCase):
    # Online version
    def test_parse_buildings(self):
        credentials = init_credentials('./tests/configs/credentials_static_cookies.json')

        own_uid = credentials.get_own_uid()
        account = Account(own_uid)
        account.update_villages(credentials)

        village = account.villages[0]
        village.force_update(credentials)
        buildings_str = str(village.buildings)

        expected = """Empty place	0 @ 0
Woodcutter	0 @ 1
Cropland	0 @ 2
Woodcutter	2 @ 3
Iron Mine	0 @ 4
Clay Pit	0 @ 5
Clay Pit	4 @ 6
Iron Mine	0 @ 7
Cropland	0 @ 8
Cropland	0 @ 9
Iron Mine	0 @ 10
Iron Mine	0 @ 11
Cropland	0 @ 12
Cropland	0 @ 13
Woodcutter	0 @ 14
Cropland	3 @ 15
Clay Pit	0 @ 16
Woodcutter	0 @ 17
Clay Pit	0 @ 18
Warehouse	1 @ 19
Granary	1 @ 20
Empty place	0 @ 21
Empty place	0 @ 22
Empty place	0 @ 23
Empty place	0 @ 24
Empty place	0 @ 25
Main Building	3 @ 26
Empty place	0 @ 27
Empty place	0 @ 28
Empty place	0 @ 29
Empty place	0 @ 30
Empty place	0 @ 31
Empty place	0 @ 32
Empty place	0 @ 33
Empty place	0 @ 34
Empty place	0 @ 35
Empty place	0 @ 36
Empty place	0 @ 37
Empty place	0 @ 38
Rally Point	0 @ 39
Empty place	0 @ 0
"""

        assert buildings_str == expected

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

        assert max(buildings).lvl == 5
        assert min(buildings).lvl == 6
