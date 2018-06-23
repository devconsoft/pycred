import unittest

from .. import GetDataFailed
from ..memory import MemoryStorage


class TestMemoryStorage(unittest.TestCase):

    data = 'data'
    user = 'user'

    def test_get_data(self):
        s = MemoryStorage()
        s.data[self.user] = self.data
        result = s.get_data(self.user)
        self.assertEqual(self.data, result)

    def test_set_data(self):
        s = MemoryStorage()
        s.set_data(self.user, self.data)
        self.assertEqual(self.data, s.data[self.user])

    def test_raises_get_data_failed(self):
        s = MemoryStorage()
        with self.assertRaises(GetDataFailed):
            s.get_data('user')
