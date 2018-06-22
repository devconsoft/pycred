import unittest

from pycred.credentials import Credentials

from .. import DeserializationFailed, SerializationFailed
from ..json import JsonSerializer


class TestJsonSerializer(unittest.TestCase):

    serialized_data = '["USERNAME", "PASSWORD"]'

    def test_serialize(self):
        s = JsonSerializer()
        c = Credentials('USERNAME', 'PASSWORD')
        result = s.serialize(c)
        self.assertEqual(self.serialized_data, result)

    def test_deserialize(self):
        s = JsonSerializer()
        result = s.deserialize(self.serialized_data)
        self.assertIsInstance(result, Credentials)
        self.assertEqual('USERNAME', result.username)
        self.assertEqual('PASSWORD', result.password)

    def test_raises_invalid_data_format_if_deserialization_fails(self):
        s = JsonSerializer()
        with self.assertRaises(DeserializationFailed):
            s.deserialize("invalid")

    def test_raises_failed_serialization_if_serialization_fails(self):
        s = JsonSerializer()
        with self.assertRaises(SerializationFailed):
            s.serialize("invalid")
