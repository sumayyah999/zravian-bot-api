# File TODOs
# TODO(@alexvelea): Add fixed positions for mainB/rally
# TODO(@alexvelea): Add support for race specific buildings
# TODO(@alexvelea): Add The rest of the buildings (extended{Rax,Stable}), Palace
# TODO(@alexvelea): Add wall support
# TODO(@alexvelea): Check for "Build a Main Building"
from functools import reduce


class BuildingType:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Buildings:
    empty = BuildingType('Empty place')

    # Economy Infrastructure
    mainB = BuildingType('Main Building')
    granary = BuildingType('Granary')
    warehouse = BuildingType('Warehouse')
    marketplace = BuildingType('Marketplace')

    # Military
    barracks = BuildingType('Barracks')
    stable = BuildingType('Stable')
    siege = BuildingType('Siege Workshop')
    rally = BuildingType('Rally Point')

    # Military infrastructure
    academy = BuildingType('Academy')
    armoury = BuildingType('Armoury')
    blacksmith = BuildingType('Blacksmith')

    # Expansion
    residence = BuildingType('Residence')
    hall = BuildingType('Town Hall')

    # Resources
    bonusWood = BuildingType('Sawmill')
    bonusClay = BuildingType('Brickworks')
    bonusIron = BuildingType('Iron Foundry')
    bonusCrop1 = BuildingType('Flour Mill')
    bonusCrop2 = BuildingType('Bakery')

    all = [
        empty,
        mainB, granary, warehouse, marketplace,
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
    def __init__(self, building, lvl, location_id):
        self.building = building
        self.lvl = lvl
        self.location_id = location_id

    def __str__(self):
        return '{0}\t{1} @ {2}'.format(self.building, self.lvl, self.location_id)


class VillageCenter:
    # Village center buildings have IDs from [19, 38]
    # Rally point has ID 39
    # Wall has ID 40
    id_offset = 19

    def __init__(self):
        self.buildings = []

    def __str__(self):
        return reduce(lambda x, y: x + y, map(lambda x: str(x) + "\n", self.buildings))


def lvl_to_int(lvl_str):
    if '+' in lvl_str:
        return int(lvl_str[0:lvl_str.find('+')])
    else:
        return int(lvl_str)


def parse_center(soup):
    all_buildings = soup.find('map', {'name': 'map2'}).findAll('area')

    vc = VillageCenter()

    for index, raw_building in enumerate(all_buildings[0:18]):
        alt_text = raw_building['alt']
        if alt_text == Buildings.empty.name:
            vc.buildings.append(BuildingInstance(Buildings.empty, lvl=0, location_id=VillageCenter.id_offset + index))
            continue

        [building_name, building_lvl] = alt_text.split(' level ')
        building = Buildings.get_by_name(building_name)
        lvl = lvl_to_int(building_lvl)

        vc.buildings.append(BuildingInstance(building, lvl, VillageCenter.id_offset + index))

    # Get Rally Point
    rally_alt_text = all_buildings[20]['alt']
    rally_id = VillageCenter.id_offset + 20

    if rally_alt_text == 'Build a Rally Point':
        vc.buildings.append(BuildingInstance(Buildings.rally, lvl=0, location_id=rally_id))
    else:
        [building_name, building_lvl] = rally_alt_text.split(' level ')
        building = Buildings.get_by_name(building_name)
        lvl = lvl_to_int(building_lvl)
        vc.buildings.append(BuildingInstance(building, lvl, rally_id))

    # Pass on wall
    return vc
