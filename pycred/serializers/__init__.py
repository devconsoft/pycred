from abc import ABCMeta, abstractmethod


class DeserializationFailed(Exception):
    """Thrown if data passed to serializer could not be properly deserialized."""
    pass


class SerializationFailed(Exception):
    """Thrown if credentials could not be properly serialized."""
    pass


class AbstractSerializer(metaclass=ABCMeta):

    @abstractmethod
    def serialize(self, credentials):
        """
        Serialize credentails.

        If serialization fails, the function should throw SerializationFailed
        exception.

        The exception is not allowed to contain any data except the name of
        the serializing class.
        """
        pass

    @abstractmethod
    def deserialize(self, data):
        """
        Deserialize data and return Credentials object.

        If deserialization fails, the method should throw DeserializationFailed
        exception.

        The exception is not allowed to contain any data except the name of the
        serializing class.
        """
        pass
