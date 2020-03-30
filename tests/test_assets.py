from unittest import TestCase
from functools import reduce
from api.assets import Building


class TestBuildingType(TestCase):
    def test_resources_for_lvl(self):
        # Main Building
        resources = reduce(lambda x, y: str(x) + '\n' + str(y),
                           map(lambda x: Building.mainB.resources_for_lvl(x), range(1, 21)))
        expected = """[70, 40, 60, 20]
[90, 50, 75, 25]
[115, 65, 100, 35]
[145, 85, 125, 40]
[190, 105, 160, 55]
[240, 135, 205, 70]
[310, 175, 265, 90]
[395, 225, 340, 115]
[505, 290, 430, 145]
[645, 370, 555, 185]
[825, 470, 710, 235]
[1060, 605, 905, 300]
[1355, 775, 1160, 385]
[1735, 990, 1485, 495]
[2220, 1270, 1900, 635]
[2840, 1625, 2435, 810]
[3635, 2075, 3115, 1040]
[4650, 2660, 3990, 1330]
[5955, 3405, 5105, 1700]
[7620, 4355, 6535, 2180]"""
        assert resources == expected

        # wood / Woodcutter
        resources = reduce(lambda x, y: str(x) + '\n' + str(y),
                           map(lambda x: Building.wood.resources_for_lvl(x), range(1, 21)))
        expected = """[40, 100, 50, 60]
[65, 165, 85, 100]
[110, 280, 140, 165]
[185, 465, 235, 280]
[310, 780, 390, 465]
[520, 1300, 650, 780]
[870, 2170, 1085, 1300]
[1450, 3625, 1810, 2175]
[2420, 6050, 3025, 3630]
[4040, 10105, 5050, 6060]
[6750, 16870, 8435, 10125]
[11270, 28175, 14090, 16905]
[18820, 47055, 23525, 28230]
[31430, 78580, 39290, 47150]
[52490, 131230, 65615, 78740]
[87660, 219155, 109575, 131490]
[146395, 365985, 182995, 219590]
[244480, 611195, 305600, 366715]
[408280, 1020695, 510350, 612420]
[681825, 1704565, 852280, 1022740]"""
        assert resources == expected

        # Max levels for weird structures
        assert str(Building.hero_mansion.resources_for_lvl(20)) == "[157865, 151095, 157865, 54125]"
        assert str(Building.bonusWood.resources_for_lvl(5)) == "[5460, 3990, 3045, 945]"
        assert str(Building.brewery.resources_for_lvl(10)) == "[30165, 19215, 25825, 35950]"
