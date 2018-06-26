import json
import logging

from pycred.credentials import Credentials

from . import AbstractSerializer, DeserializationFailed, SerializationFailed

logger = logging.getLogger('JsonSerializer')
logger.addHandler(logging.NullHandler())


class JsonSerializer(AbstractSerializer):

    def serialize(self, credentials):
        try:
            data = [credentials.username, credentials.password]
            return json.dumps(data)
        except Exception:
            raise SerializationFailed('JsonSerializer') from None

    def deserialize(self, data):
        try:
            deserialized = json.loads(data)
            return Credentials(deserialized[0], deserialized[1])
        except Exception:
            raise DeserializationFailed('JsonSerializer') from None

    def delete(self):
        logger.debug("Deleted")
