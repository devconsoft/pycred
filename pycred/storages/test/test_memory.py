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

    def test_unset_data(self):
        s = MemoryStorage()
        s.data[self.user] = self.data
        s.unset_data(self.user)
        with self.assertRaises(InvalidUser):
            s.get_data('user')

    def test_raises_invaliduser_if_the_user_does_not_exists(self):
        s = MemoryStorage()
        with self.assertRaises(InvalidUser):
            s.get_data('user')

    def test_get_users_returns_sorted_list(self):
        s = MemoryStorage()
        s.set_data('user2', self.data)
        s.set_data('user1', self.data)
        users = s.get_users()
        self.assertEqual(['user1', 'user2'], users)
