from bs4 import BeautifulSoup


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
