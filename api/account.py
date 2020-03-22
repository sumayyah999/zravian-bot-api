class Account:
    def __init__(self, uid):
        self.uid = uid

    def update_villages(self, credentials):
        soup = credentials.call("profile.php", {'uid': self.uid})
        return parse_profile_page(soup)


def parse_profile_page(soup):
    villages = []
    for raw_village in soup.find('table', {'id': 'villages'}).find('tbody').findAll('tr'):
        name = raw_village.find('td', {'class': 'nam'}).find('a').string
        vid = raw_village.find('td', {'class': 'hab'}).string
        villages.append((name, vid))

    return villages
