from functools import total_ordering

import assets
from .assets import Building
from .credentials import Page
import utils


@total_ordering
class BuildingInstance(assets.BuildingType):
    # plus_lvl refers to the number of levels under construction
    def __init__(self, building, lvl, plus_lvl, location_id):
        super().__init__(whole_object=building)

        self.lvl = lvl
        self.plus_lvl = plus_lvl
        self.location_id = location_id

    def __str__(self):
        return '({0} - lvl:{1} id:{2})'.format(
            super().__str__(),
            self.lvl if self.plus_lvl == 0 else f'{self.lvl}+{self.plus_lvl}',
            self.location_id)

    def __repr__(self):
        return f'Building({self.__str__()})'

    # For comparing BuildingInstance with BuildingInstance
    # - The ordering is done looking only at the lvl.
    # - This enables a workflow where you can select the 'min' or 'max' of multiple buildings based on lvl
    # For comparing BuildingInstance with BuildingType
    # - return True if the 2 buildings are of the same type

    def __eq__(self, other):
        if type(other) == assets.BuildingType:
            return self.bid == other.bid
        elif type(other) == BuildingInstance:
            return self.lvl + self.plus_lvl == other.lvl + other.plus_lvl
        else:
            raise Exception()

    def __lt__(self, other):
        return (self.lvl + self.plus_lvl) < (other.lvl + other.plus_lvl)

    def resources_to_upgrade(self):
        return self.resources_for_lvl(self.lvl + self.plus_lvl + 1)

    def is_max_lvl(self):
        return self.max_level >= self.plus_lvl + self.lvl

    def update(self, oth):
        self.__dict__.update(oth.__dict__)


class VillageBuildings:
    # Rally point has ID 39
    # Wall has ID 40
    overview_offset = 1
    center_offset = 19

    def __init__(self, village):
        self.village = village
        self.buildings = [BuildingInstance(Building.empty, 0, 0, 0) for _ in range(41)]

    def __str__(self):
        return self.buildings

    def __repr__(self):
        return f'Buildings({self.buildings})'

    def __getitem__(self, key):
        return self.buildings[key]

    def find(self, building):
        return list(filter(lambda x: x.name == building.name, self.buildings))

    def update_from_soup(self, soup):
        if soup.page == Page.overview:
            offset = self.overview_offset
            u = parse_overview(soup)
        elif soup.page == Page.center:
            offset = self.center_offset
            u = parse_center(soup)
        else:
            return False

        for index, new_b in enumerate(u):
            self.buildings[offset + index].update(new_b)
        return True


def append_building(buildings, alt_text, index):
    [building_name, building_lvl] = alt_text.split(' level ')
    building = Building.get_by_name(building_name)
    (lvl, plus_lvl) = utils.lvl_to_int(building_lvl)
    buildings.append(BuildingInstance(building, lvl, plus_lvl, index))


def parse_overview(soup):
    buildings = []
    for index, raw_res in enumerate(soup.findAll('area', {'shape': 'circle'})[0:18]):
        append_building(buildings, raw_res['alt'], index + VillageBuildings.overview_offset)

    return buildings


def parse_center(soup):
    all_buildings = soup.find('map', {'name': 'map2'}).findAll('area')
    buildings = []

    for index, raw_building in enumerate(all_buildings[0:20]):
        alt_text = raw_building['alt']
        if alt_text == Building.empty.name:
            buildings.append(
                BuildingInstance(Building.empty, lvl=0, plus_lvl=0, location_id=VillageBuildings.center_offset + index))
            continue
        append_building(buildings, alt_text, index + VillageBuildings.center_offset)

    # Get Rally Point
    rally_alt_text = all_buildings[20]['alt']
    rally_id = VillageBuildings.center_offset + 20

    if rally_alt_text == 'Build a Rally Point':
        buildings.append(BuildingInstance(Building.rally, lvl=0, plus_lvl=0, location_id=rally_id))
    else:
        append_building(buildings, rally_alt_text, rally_id)

    # Pass on wall
    return buildings
