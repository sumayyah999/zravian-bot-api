import requests
from bs4 import BeautifulSoup
from functools import reduce


class Account:
    def __init__(self, config):
        self.config = config

    def update_villages(self):
        soup = self.call("profile.php")
        return parse_profile_page(soup)

    def call(self, page):
        url = self.config.url + page
        # if len(get_dict):
        #     url = url + "?" + reduce(lambda x, y: x + y,
        #                              map(lambda x: '&{0}={1}'.format(str(x[0]), str(x[1])), get_dict.items()))[1:]

        r = requests.post(url, cookies=self.config.cookies)
        return BeautifulSoup(r.content, 'html.parser')


def parse_profile_page(soup):
    villages = []
    for raw_village in soup.find('table', {'id': 'villages'}).find('tbody').findAll('tr'):
        name = raw_village.find('td', {'class': 'nam'}).find('a').string
        vid = raw_village.find('td', {'class': 'hab'}).string
        villages.append((name, vid))

    return villages
