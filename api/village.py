import re

from .village_center import VillageCenter
from .village_resources import VillageResources
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

        self.buildings = []
        self.resources = VillageResources(0)
        self.center = VillageCenter()
        self.k = None

    def __str__(self):
        return "{0} ({1},{2})".format(self.name, self.x, self.y)

    def force_update(self, credentials):
        self.update_from_soup(credentials.call(Page.overview, params={'vid': self.vid}))
        self.update_from_soup(credentials.call(Page.center, params={'vid': self.vid}))

    def update_from_soup(self, soup):
        new_k = parse_k(soup)
        self.k = self.k if new_k is None else new_k

        self.account.events.update_from_soup(soup, village=self)
        if soup.page == Page.overview:
            self.resources.update_from_soup(soup)
        if soup.page == Page.center:
            self.center.update_from_soup(soup)

        self.buildings = [None] + self.resources.buildings + self.center.buildings


def parse_k(soup):
    soup_str = str(soup)
    index = soup_str.find("&amp;k=")
    if index == -1:
        return None
    return soup_str[index + 7:index + 7 + 5]


# TODO(@alexvelea) Should I deprecate this?
# Given a page, it returns the vid of the selected village or None if the account has only 1 village
def parse_current_vid(soup):
    side_info = soup.find('div', {'id': 'side_info'})
    if side_info is None:
        return None

    vid_link = side_info.find('a', {'style': 'text-decoration:underline'})
    # href="?vid=4007"
    return int(re.search('\?vid=(.*)', vid_link['href']).group(1))
