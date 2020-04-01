import json
import requests
from bs4 import BeautifulSoup
from functools import reduce


class BadLogin(Exception):
    pass


class BadCookies(Exception):
    pass


class BadCredentialsFile(Exception):
    no_url = 0
    no_cookies_or_login = 1
    incomplete_login = 2
    fallback_with_no_login = 3

    def __init__(self, e_type):
        self.e_type = e_type


class Page:
    overview = "village1.php"
    center = "village2.php"
    profile = "profile.php"
    building = "build.php"
    move_troops = "v2v.php"


class Credentials:
    def __init__(self, url, cookies):
        self.url = url
        self.cookies = cookies

    @classmethod
    def by_login(cls, url, login_info):
        session = requests.Session()
        response = session.get(url)
        bs = BeautifulSoup(response.content, 'html.parser')
        serv = (bs.find('input', {'name': 'serv'}))['value']

        cookies = session.cookies.get_dict()

        data = {
            'name': login_info['username'],
            'pass': login_info['password'],
            'serv': serv
        }

        response = session.post(url, cookies=cookies, data=data)
        bs = BeautifulSoup(response.content, 'html.parser')
        session.close()

        if bs.find('fieldset', {'class': 'err'}):
            raise BadLogin

        return Credentials(url, cookies)

    def cookies_to_str(self):
        return reduce(lambda x, y: x + '; ' + y, map(lambda p: p[0] + "=" + p[1], self.cookies.items()))

    def get_own_uid(self):
        soup = self.call(Page.profile)
        node = soup.find('input', {'name': 'uid'})
        if node:
            return int(node['value'])
        else:
            return None

    def call(self, page, params=None, data=None):
        url = self.url + page
        r = requests.post(url, cookies=self.cookies, params=params, data=data)
        soup = BeautifulSoup(r.content, 'html.parser')
        soup.page = page
        soup.params = params
        soup.data = data
        return soup


def init_credentials(credentials_file_path, write_new_cookies=True):
    with open(credentials_file_path) as json_file:
        data = json.load(json_file)

    data['credentials_file_path'] = credentials_file_path
    return parse_credentials(data, write_new_cookies)


def parse_credentials(json_data, write_new_cookies=True):
    if 'url' not in json_data:
        # No URL specified
        raise BadCredentialsFile(BadCredentialsFile.no_url)

    if 'cookies' not in json_data and 'login_info' not in json_data:
        # 'cookies' or 'login_info' not specified in credentials file
        raise BadCredentialsFile(BadCredentialsFile.no_cookies_or_login)

    if 'login_info' in json_data:
        if 'username' not in json_data['login_info'] or 'password' not in json_data['login_info']:
            # Login info provided without data
            raise BadCredentialsFile(BadCredentialsFile.incomplete_login)

    fallback_on_login = json_data.get('fallback_on_login', False)
    if fallback_on_login is True and 'login_info' not in json_data:
        raise BadCredentialsFile(BadCredentialsFile.fallback_with_no_login)

    if 'cookies' in json_data:
        cookies_str = json_data['cookies']
        cookies = dict()
        for itr in cookies_str.split('; '):
            aux = itr.split('=')
            cookies[aux[0]] = aux[1]

        credentials = Credentials(json_data['url'], cookies)
        if credentials.get_own_uid() is None:
            if fallback_on_login is False:
                raise BadCookies
            else:
                print("Bad cookies! Trying to login using username+password")
        else:
            return credentials

    credentials = Credentials.by_login(json_data['url'], json_data['login_info'])
    if 'credentials_file_path' in json_data and write_new_cookies:
        # Rewrite cookies in original file
        json_data['fallback_on_login'] = True
        json_data['cookies'] = credentials.cookies_to_str()
        path = json_data.pop('credentials_file_path')
        with open(path, 'w+') as outfile:
            json.dump(json_data, outfile, indent=2, sort_keys=True)
            outfile.close()

    return credentials
