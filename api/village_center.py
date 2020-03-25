from functools import reduce
import utils


# TODO(@alexvelea) Move this class to an assets file
# TODO(@alexvelea) Add some more info, such as
# - capital only
# - max level
# - multiple build? (for granary, warehouse)
# - requirements?
class BuildingType:
    def __init__(self, name, bid):
        self.name = name
        self.id = bid

    def __str__(self):
        return self.name


# TODO(@alexvelea) Add The rest of the buildings extended Rax, Palace, wall as well as race-specific buildings
class Buildings:
    empty = BuildingType('Empty place', 0)

    # Economy Infrastructure
    mainB = BuildingType('Main Building', 15)
    granary = BuildingType('Granary', 11)
    warehouse = BuildingType('Warehouse', 10)
    marketplace = BuildingType('Marketplace', 17)
    cranny = BuildingType('Cranny', 23)

    # Military
    barracks = BuildingType('Barracks', 19)
    stable = BuildingType('Stable', 20)
    siege = BuildingType('Siege Workshop', 21)
    rally = BuildingType('Rally Point', 16)

    # Military infrastructure
    academy = BuildingType('Academy', 22)
    armoury = BuildingType('Armoury', 13)
    blacksmith = BuildingType('Blacksmith', 12)

    # Expansion
    residence = BuildingType('Residence', 25)
    hall = BuildingType('Town Hall', 24)

    # Resources
    bonusWood = BuildingType('Sawmill', 5)
    bonusClay = BuildingType('Brickworks', 6)
    bonusIron = BuildingType('Iron Foundry', 7)
    bonusCrop1 = BuildingType('Flour Mill', 8)
    bonusCrop2 = BuildingType('Bakery', 9)

    all = [
        empty,
        mainB, granary, warehouse, marketplace, cranny,
        barracks, stable, siege, rally,
        academy, armoury, blacksmith,
        residence, hall,
        bonusWood, bonusClay, bonusIron, bonusCrop1, bonusCrop2
    ]

    @classmethod
    def get_by_name(cls, building_name):
        [building] = filter(lambda x: x.name == building_name, cls.all)
        return building


class BuildingInstance:
    # plus_lvl refers to the number of levels under construction
    def __init__(self, building, lvl, plus_lvl, location_id):
        self.building = building
        self.lvl = lvl
        self.plus_lvl = plus_lvl
        self.location_id = location_id

    def __str__(self):
        return '{0}\t{1} @ {2}'.format(self.building,
                                       self.lvl if self.plus_lvl == 0 else "{0}+{1}".format(self.lvl, self.plus_lvl),
                                       self.location_id)


# TODO(@alexvelea) Merge this with a subpart of VillageResources
class VillageCenter:
    # Village center buildings have IDs from [19, 38]
    # Rally point has ID 39
    # Wall has ID 40
    url = 'village2.php'
    id_offset = 19

    def __init__(self):
        self.buildings = []

    def __str__(self):
        return reduce(lambda x, y: x + y, map(lambda x: str(x) + "\n", self.buildings))

    def find(self, building):
        return list(filter(lambda x: x.building.name == building.name, self.buildings))

    def update_from_soup(self, soup):
        nc = parse_center(soup)
        self.buildings = nc.buildings


def parse_center(soup):
    all_buildings = soup.find('map', {'name': 'map2'}).findAll('area')

    vc = VillageCenter()

    for index, raw_building in enumerate(all_buildings[0:18]):
        alt_text = raw_building['alt']
        if alt_text == Buildings.empty.name:
            vc.buildings.append(BuildingInstance(Buildings.empty, lvl=0, plus_lvl=0, location_id=VillageCenter.id_offset + index))
            continue

        [building_name, building_lvl] = alt_text.split(' level ')
        building = Buildings.get_by_name(building_name)
        (lvl, plus_lvl) = utils.lvl_to_int(building_lvl)
        vc.buildings.append(BuildingInstance(building, lvl, plus_lvl, VillageCenter.id_offset + index))

    # Get Rally Point
    rally_alt_text = all_buildings[20]['alt']
    rally_id = VillageCenter.id_offset + 20

    if rally_alt_text == 'Build a Rally Point':
        vc.buildings.append(BuildingInstance(Buildings.rally, lvl=0, plus_lvl=0, location_id=rally_id))
    else:
        [building_name, building_lvl] = rally_alt_text.split(' level ')
        building = Buildings.get_by_name(building_name)
        (lvl, plus_lvl) = utils.lvl_to_int(building_lvl)
        vc.buildings.append(BuildingInstance(building, lvl, plus_lvl, rally_id))

    # Pass on wall
    return vc
