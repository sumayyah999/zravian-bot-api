from unittest import TestCase

from tests.utils import *
from api.buildings import BuildingInstance, Building


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
