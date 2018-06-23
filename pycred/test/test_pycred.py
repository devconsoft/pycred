import unittest
from unittest.mock import patch

from ..credentials import Credentials
from ..pycred import get_store
from ..storages.memory import MemoryStorage


class TestPyCredLib(unittest.TestCase):

    def test_get_store(self):
        mem = MemoryStorage()
        with patch('pycred.factory.Factory.get_storage', return_value=mem):
            user = 'user'
            cred = Credentials('USERNAME', 'PASSWORD')
            mem.set_data(user, '["USERNAME", "PASSWORD"]')
            store = get_store('store')
            result = store.get_credentials(user)
            self.assertEqual(cred.username, result.username)
            self.assertEqual(cred.password, result.password)

    def xtest_clear_json_file(self):
        assert False, "not implemented"
