import re
import time

import utils
from credentials import Page
from assets import Building


class EventInstance:
    def __init__(self, event_type, village, in_time, at_time):
        self.event_type = event_type
        self.finish_timestamp = time.time() + utils.countdown_to_sec(in_time)
        self.at_time = at_time
        self.village = village

    def __eq__(self, other):
        return self.event_type == other.event_type and \
               self.at_time == other.at_time and \
               self.village.vid == other.village.vid

    def __lt__(self, other):
        return self.finish_timestamp < other.finish_timestamp

    def __str__(self):
        return self.event_type + " at " + self.at_time + " in " + str(self.village)


class EventQueue:
    BuildingFinished = "BuildingFinished"
    BuildingDemolished = "BuildingDemolished"
    CelebrationCompleted = "CelebrationCompleted"
    TradersArrived = "TradersArrived"

    def __init__(self):
        self.queue = []

    def broadcast_finished_events(self):
        current_time = time.time()
        if len(self.queue) and self.queue[0].finish_timestamp < current_time:
            print("Broadcast ", str(self.queue[0]))
            self.queue = self.queue[1:]
            return 1 + self.broadcast_finished_events()

        return 0

    def update_from_soup(self, soup, village):
        events = []
        if soup.page == Page.building and village.buildings[soup.params['id']] == Building.mainB:
            events += parse_main_building_queue(soup, village)

        if soup.page == Page.building and village.buildings[soup.params['id']] == Building.hall:
            events += parse_town_hall_queue(soup, village)

        if soup.page == Page.building and village.buildings[soup.params['id']] == Building.marketplace:
            events += parse_market_queue(soup, village)

        if soup.page == Page.overview or soup.page == Page.center:
            events += parse_building_construction_queue(soup, village)

        self.queue += [x for x in events if x not in self.queue]
        self.queue.sort()


def parse_town_hall_queue(soup, village):
    b_table = soup.find('table', {'class': 'under_progress'})
    if b_table is None:
        return []

    in_time = b_table.find('span', {'id': 'timer1'}).text
    at_time = utils.at_time_from_in_time(soup, in_time=in_time)

    return [EventInstance(EventQueue.CelebrationCompleted, village, in_time, at_time)]


def parse_market_queue(soup, village):
    traders = soup.findAll('table', {'class': 'traders'})
    eq = []

    for trader_soup in traders:
        returning = len(trader_soup.findAll('span', {'class': 'none'})) == 1

        if returning:
            continue

        target_village_soup = trader_soup.find('thead').findAll('a')[1]
        target_village_vid = int(re.search('.*id=(.*)', target_village_soup['href']).group(1))

        in_time = trader_soup.find('span', {'id': 'timer1'}).text
        at_time = utils.at_time_from_in_time(soup, in_time=in_time)

        eq.append(EventInstance(EventQueue.TradersArrived, village, in_time, at_time))

    return eq


def parse_main_building_queue(soup, village):
    b_table = soup.find('table', {'id': 'demolish'})
    if b_table is None:
        return []

    in_time = b_table.find('span', {'id': 'timer1'}).text
    at_time = utils.at_time_from_in_time(soup, in_time=in_time)

    return [EventInstance(EventQueue.BuildingDemolished, village, in_time, at_time)]


def parse_building_construction_queue(soup, village):
    b_table = soup.find('table', {'id': 'building_contract'})

    # check for empty queue
    if b_table is None:
        return []

    buildings = b_table.find('tbody').find_all('tr')
    eq = []

    for building in buildings:
        tds = building.findAll('td')

        # Useful if in the future we want to capture the building and lvl as well
        # q = re.search('(.*) \(level (.*)\)', tds[1].find('a').text)
        # name = q.group(1)
        # lvl = int(q.group(2))

        q = re.search('Finished in (.*) at (.*)', tds[2].text)
        in_time = q.group(1)
        at_time = q.group(2)

        eq.append(EventInstance(EventQueue.BuildingFinished, village, in_time, at_time))

    return eq
