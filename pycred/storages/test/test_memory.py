import unittest

from .. import InvalidUser
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

    def test_raises_invaliduser_if_the_user_does_not_exists(self):
        s = MemoryStorage()
        with self.assertRaises(InvalidUser):
            s.get_data('user')
