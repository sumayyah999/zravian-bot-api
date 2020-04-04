import re

from .buildings import VillageBuildings
from .resources import VillageResources
from .credentials import Page


def coords_from_vid(vid):
    vid -= 1
    y = vid % 200
    if y > 100:
        y = y - 200
    x = vid // 200
    if x > 100:
        x = x - 200
    return x, y


def vid_from_coords(x, y):
    if x < 0:
        vid = 200 * (200 + x)
    else:
        vid = 200 * x
    if y < 0:
        vid += (200 + y)
    else:
        vid += y
    return vid + 1


class Village:
    def __init__(self, account, vid, name):
        self.account = account
        self.vid = vid
        self.name = name
        [self.x, self.y] = coords_from_vid(self.vid)

        self.buildings = VillageBuildings(self)
        self.resources = VillageResources(self)
        self.k = None

    def __str__(self):
        return f'{self.vid}'

    def __repr__(self):
        return f'Village({self.name} ({self.x}, {self.y}))'

    def force_update(self, credentials):
        self.update_from_soup(credentials.call(Page.overview, params={'vid': self.vid}))
        self.update_from_soup(credentials.call(Page.center, params={'vid': self.vid}))

    def update_from_soup(self, soup):
        new_k = parse_k(soup)
        self.k = self.k if new_k is None else new_k

        # TODO: move this update into account
        self.account.events.update_from_soup(soup, village=self)
        self.buildings.update_from_soup(soup)
        self.resources.update_from_soup(soup)


def parse_k(soup):
    soup_str = str(soup)
    index = soup_str.find('&amp;k=')
    if index == -1:
        return None
    return soup_str[index + 7:index + 7 + 5]
