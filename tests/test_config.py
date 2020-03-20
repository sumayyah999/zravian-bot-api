from unittest import TestCase
from api.config import init_config


class Test(TestCase):
    def test_init_config(self):
        if init_config("./configs/main_config.json") is None:
            assert False
