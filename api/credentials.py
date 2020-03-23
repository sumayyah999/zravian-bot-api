# TODO(@alexvelea): Add more tests to test for failures
import json
import requests
from bs4 import BeautifulSoup
from functools import reduce


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
            # TODO(@alexvelea): make this an exception
            print('Bad login!')
            return None

        return Credentials(url, cookies)

    def get_own_uid(self):
        soup = self.call("profile.php")
        return int(soup.find('input', {'name': 'uid'})['value'])

    def call(self, page, params=None, data=None):
        url = self.url + page
        r = requests.post(url, cookies=self.cookies, params=params, data=data)
        soup = BeautifulSoup(r.content, 'html.parser')
        soup.page = page
        return soup


def init_credentials(credentials_file_path):
    with open(credentials_file_path) as json_file:
        data = json.load(json_file)

        ok = True
        if 'url' not in data:
            # TODO(@alexvelea): make this an exception
            print('URL not specified in credentials file')
            ok = False

        if 'cookies' not in data and 'login_info' not in data:
            # TODO(@alexvelea): make this an exception
            print("'cookies' or 'login_info' not specified in credentials file")
            return None

        if 'login_info' in data:
            if 'username' not in data['login_info'] or 'password' not in data['login_info']:
                # TODO(@alexvelea): make this an exception
                print("Login info provided without data")
                ok = False

        if not ok:
            return None

        if 'cookies' in data:
            cookies_str = data['cookies']
            cookies = dict()
            for itr in cookies_str.split('; '):
                aux = itr.split('=')
                cookies[aux[0]] = aux[1]

            return Credentials(data['url'], cookies)

        if 'username' in data['login_info'] and 'password' in data['login_info']:
            return Credentials.by_login(data['url'], data['login_info'])

        return None
