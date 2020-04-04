from bs4 import BeautifulSoup
from api.account import Account
from api.village import Village
from api.credentials import Page


def assert_str(a, b):
    ra = repr(a)
    if type(b) == str:
        rb = b
    else:
        rb = repr(b)

    if not (ra == rb):
        print(f'Got |{ra}| but expected |{rb}|')
        assert False


def assert_eq(a, b):
    if not (a == b):
        print(f'Excepted {a} == {b}')
        assert False


def assert_lt(a, b):
    if not (a < b):
        print(f'Excepted {a} < {b}')
        assert False


def assert_le(a, b):
    if not (a <= b):
        print(f'Expected {a} <= {b}')
        assert False


def soup_from_file(file_path):
    with open(file_path, 'r') as content_file:
        content = content_file.read()
        soup = BeautifulSoup(content, 'html.parser')
        return soup


def get_dumped_account():
    soup_overview = soup_from_file('./tests/configs/village1_html_dump.txt')
    soup_overview.page = Page.overview

    soup_center = soup_from_file('./tests/configs/village2_html_dump.txt')
    soup_center.page = Page.center

    account = Account(0)
    village = Village(account, 0, '')
    village.update_from_soup(soup_overview)
    village.update_from_soup(soup_center)
    account.villages = [village]

    return account