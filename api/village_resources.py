import time
import utils


class ResourceType:
    def __init__(self, name, res_id):
        self.id = res_id
        self.name = name

    def __str__(self):
        return self.name


class Resources:
    wood = ResourceType('Woodcutter', 1)
    clay = ResourceType('Clay Pit', 2)
    iron = ResourceType('Iron Mine', 3)
    crop = ResourceType('Cropland', 4)

    @classmethod
    def get_by_name(cls, name):
        for res in [cls.wood, cls.clay, cls.iron, cls.crop]:
            if name == res.name:
                return res


class ResourceInstance:
    # plus_lvl refers to the number of levels under construction
    def __init__(self, resource, lvl, plus_lvl, location_id):
        self.resource = resource
        self.lvl = lvl
        self.plus_lvl = plus_lvl
        self.location_id = location_id

    def __str__(self):
        return "{0}\t{1} @ {2}".format(self.resource,
                                       self.lvl if self.plus_lvl == 0 else "{0}+{1}".format(self.lvl, self.plus_lvl),
                                       self.location_id)


# TODO(@alexvelea) Merge self.buildings this with VillageCenter
class VillageResources:
    url = 'village1.php'
    id_offset = 1

    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.buildings = []
        self.production = [0, 0, 0, 0]

        self.stored = [0, 0, 0, 0]
        self.capacity = [0, 0, 0, 0]
        self.wheat_consumption = 0

    def __str__(self):
        s = ""
        for location in self.buildings:
            s = s + str(location) + "\n"
        s = s + "production: {0}\n".format(self.production)
        s = s + "stored: {0}\n".format(self.stored)
        s = s + "capacity: {0}\n".format(self.capacity)
        s = s + "wheat_consumption: {0}\n".format(self.wheat_consumption)
        return s

    def update_from_soup(self, soup):
        nc = parse_resources(soup)
        self.timestamp = nc.timestamp
        self.buildings = nc.buildings
        self.production = nc.production

        self.stored = nc.stored
        self.capacity = nc.capacity
        self.wheat_consumption = nc.wheat_consumption


def parse_resources(soup):
    village = VillageResources(time.time())

    for index, raw_res in enumerate(soup.findAll('area', {'shape': 'circle'})[0:18]):
        [res_name, res_lvl] = str(raw_res.get('alt')).split(' level ')
        res = Resources.get_by_name(res_name)
        lvl, plus_lvl = utils.lvl_to_int(res_lvl)

        instance = ResourceInstance(res, lvl, plus_lvl, index + 1)
        village.buildings.append(instance)

    for index, raw_res in enumerate(soup.find('table', {'id': 'production'}).findAll('td', {'class': 'num'})):
        prod_str = raw_res.string
        prod = 0
        for part in prod_str.split(','):
            prod = prod * 1000 + int(part)

        village.production[index] = prod

    [stored, consumption] = soup.find('div', {'id': 'resWrap'}).findAll('tr')
    for index, raw_prod in enumerate(stored.findAll('td')[1::+2]):
        [stored, capacity] = raw_prod.string.split('/')
        village.stored[index] = int(stored)
        village.capacity[index] = int(capacity)

    [wheat_consumption, wheat_production] = consumption.findAll('td')[2].string.split('/')
    village.wheat_consumption = int(wheat_consumption)
    return village
