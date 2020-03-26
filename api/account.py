from .village import Village, vid_from_coords
from .event_queue import EventQueue
from .credentials import Page


class Account:
    def __init__(self, uid):
        self.uid = uid
        self.villages = []
        self.events = EventQueue()

    def get_village_by_vid(self, vid):
        return next(filter(lambda x: x.vid == vid, self.villages), None)

    def update_villages(self, credentials):
        soup = credentials.call(Page.profile, {'uid': self.uid})
        new_villages = parse_profile_page(soup)

        # Merge villages
        for vil in new_villages:
            [name, vid] = vil
            if vid in [x.vid for x in self.villages]:
                continue

            # add new village to our list
            self.villages.append(Village(self, vid, name))

    def __str__(self):
        return map(lambda x: str(x), self.villages)


def parse_profile_page(soup):
    villages = []
    for raw_village in soup.find('table', {'id': 'villages'}).find('tbody').findAll('tr'):
        name = raw_village.find('td', {'class': 'nam'}).find('a').string
        vid_x = int(raw_village.find('div', {'class': 'cox'}).string[1:])
        vid_y = int(raw_village.find('div', {'class': 'coy'}).string[:-1])
        vid = vid_from_coords(vid_x, vid_y)

        villages.append((name, int(vid)))

    return villages
