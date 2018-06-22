import json

from pycred.credentials import Credentials

from . import AbstractSerializer, DeserializationFailed, SerializationFailed


class JsonSerializer(AbstractSerializer):

    def serialize(self, credentials):
        try:
            data = [credentials.username, credentials.password]
            return json.dumps(data)
        except Exception:
            raise SerializationFailed('JsonSerializer')

    def deserialize(self, data):
        try:
            deserialized = json.loads(data)
            return Credentials(deserialized[0], deserialized[1])
        except Exception:
            raise DeserializationFailed('JsonSerializer')
