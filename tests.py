import unittest

from parsing import check_access


class TestAccess(unittest.TestCase):
    def setUp(self):
        self.url = 'https://www.wildberries.ru/'
        self.waited_result = True
        self.test_func = check_access

    def test_all(self):
        self.assertEqual(self.test_func(self.url), self.waited_result)


if __name__ == '__main__':
    unittest.main()
