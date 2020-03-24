import re
import time
import utils


class EventInstance:
    def __init__(self, event_type, village, time_left, finish_at):
        self.event_type = event_type
        self.finish_timestamp = time.time() + utils.countdown_to_sec(time_left)
        self.finish_at = finish_at
        self.village = village

    def __eq__(self, other):
        return self.event_type == other.event_type and \
               self.finish_at == other.finish_at and \
               self.village.vid == other.village.vid

    def __lt__(self, other):
        return self.finish_timestamp < other.finish_timestamp

    def __str__(self):
        return self.event_type + " at " + self.finish_at + " in " + str(self.village)


class EventQueue:
    BuildingFinished = "BuildingFinished"

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
        events = parse_buildings_queue(soup, village)
        self.broadcast_finished_events()

        self.queue += [x for x in events if x not in self.queue]
        self.queue.sort()


def parse_buildings_queue(soup, village):
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
        time_left = q.group(1)
        finish_at = q.group(2)

        eq.append(EventInstance(EventQueue.BuildingFinished, village, time_left, finish_at))

    return eq
