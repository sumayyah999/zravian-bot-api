# TODO(@alexvelea): Add more tests to test for failures
import json
import requests
from bs4 import BeautifulSoup


class BadLogin(Exception):
    pass


class BadCookies(Exception):
    pass


class BadCredentialsFile(Exception):
    no_url = 0
    no_cookies_or_login = 1
    incomplete_login = 2

    def __init__(self, e_type):
        self.e_type = e_type


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

    def get_own_uid(self):
        soup = self.call("profile.php")
        node = soup.find('input', {'name': 'uid'})
        if node:
            return int(node['value'])
        else:
            return None

    # TODO(@alexvelea) add a page enum
    def call(self, page, params=None, data=None):
        url = self.url + page
        r = requests.post(url, cookies=self.cookies, params=params, data=data)
        soup = BeautifulSoup(r.content, 'html.parser')
        soup.page = page
        return soup


# TODO(@alexvelea) Dump new cookies in config if login with username+password
# TODO(@alexvelea) Add a new 'fallback_on_login' = true/false in case cookies are wrong to force-create new ones
def init_credentials(credentials_file_path):
    with open(credentials_file_path) as json_file:
        data = json.load(json_file)

        if 'url' not in data:
            # No URL specified
            raise BadCredentialsFile

        if 'cookies' not in data and 'login_info' not in data:
            # 'cookies' or 'login_info' not specified in credentials file
            raise BadCredentialsFile

        if 'login_info' in data:
            if 'username' not in data['login_info'] or 'password' not in data['login_info']:
                # Login info provided without data
                raise BadCredentialsFile

        if 'cookies' in data:
            cookies_str = data['cookies']
            cookies = dict()
            for itr in cookies_str.split('; '):
                aux = itr.split('=')
                cookies[aux[0]] = aux[1]

            credentials = Credentials(data['url'], cookies)
            if credentials.get_own_uid() is None:
                # Invalid cookies. Delete them to fallback to basic-login
                raise BadCookies

            return credentials

        return Credentials.by_login(data['url'], data['login_info'])
