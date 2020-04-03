import time

from .utils import comma_number_to_int
from .credentials import Page


class VillageResources:
    id_offset = 1

    def __init__(self, village):
        self.village = village
        self.timestamp = time.time()
        self.production = [0, 0, 0, 0]

        self.stored = [0, 0, 0, 0]
        self.capacity = [0, 0, 0, 0]

    def __str__(self):
        return f'prod:{self.production}, stored:{self.stored}, capacity:{self.capacity}'

    def __repr__(self):
        return f'VilResources({self.__str__()})'

    def update_from_soup(self, soup):
        self.timestamp = time.time()

        if soup.page == Page.overview:
            nc = parse_own(soup)
            self.production = nc.production
            self.stored = nc.stored
            self.capacity = nc.capacity
        else:
            nc = parse_own(soup)
            self.stored = nc.stored
            self.capacity = nc.capacity


def parse_own(soup):
    village = VillageResources(time.time())

    production_dom = soup.find('table', {'id': 'production'})
    if production_dom is not None:
        for index, raw_res in enumerate(production_dom.findAll('td', {'class': 'num'})):
            prod_str = raw_res.string
            village.production[index] = comma_number_to_int(prod_str)

    [stored, _] = soup.find('div', {'id': 'resWrap'}).findAll('tr')
    for index, raw_prod in enumerate(stored.findAll('td')[1::+2]):
        [stored, capacity] = raw_prod.string.split('/')
        village.stored[index] = int(stored)
        village.capacity[index] = int(capacity)

    return village
