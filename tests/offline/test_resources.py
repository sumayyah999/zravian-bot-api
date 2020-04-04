from unittest import TestCase

from tests.utils import *
from api.resources import parse_own


class Test(TestCase):
    def test_parse_resources(self):
        account = get_dumped_account()
        village = account.villages[0]

        expected = 'VilResources(prod:[768000, 487680, 207360, -31859], ' \
                   'stored:[15344637, 15336994, 13943287, 6990105], ' \
                   'capacity:[15360000, 15360000, 15360000, 10240000])'

        assert_str(village.resources, expected)
