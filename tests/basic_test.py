from unittest import TestCase
import api


class Test(TestCase):
    def test_function_to_test(self):
        assert api.test.function_to_test(10) == 11

    def test_function_to_test_2(self):
        assert api.test.function_to_test_2(10) == 9
