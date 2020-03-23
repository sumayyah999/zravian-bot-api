from village_center import VillageCenter
from village_resources import VillageResources

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
        self.k = ""

    def __str__(self):
        return "{0} ({1},{2})".format(self.name, self.x, self.y)

    def force_update(self, credentials):
        self.update_from_soup(credentials.call('village1.php'))
        self.update_from_soup(credentials.call('village2.php'))

    def update_from_soup(self, soup):
        self.k = parse_k(soup)
        if soup.page == 'village1.php':
            self.resources.update_from_soup(soup)
        if soup.page == 'village2.php':
            self.center.update_from_soup(soup)

        self.buildings = [None] + self.resources.buildings + self.center.buildings


def parse_k(soup):
    soup_str = str(soup)
    index = soup_str.find("&amp;k=")
    if index == -1:
        raise Exception
    return soup_str[index + 7:index + 7 + 5]
