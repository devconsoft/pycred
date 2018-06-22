from abc import ABCMeta, abstractmethod


class GetDataFailed(Exception):
    """Thrown if data could not be retrieved from storage."""
    pass


class SetDataFailed(Exception):
    """Thrown if data passed to storage could not be stored."""
    pass


class InvalidUser(Exception):
    """Thrown if the specified user is invalid."""
    pass


class AbstractStorage(metaclass=ABCMeta):

    @abstractmethod
    def get_data(self, user):
        """
        Get data for user from storage.

        If the specified user does not exist, or is otherwise invalid, the method
        should throw InvalidUser exception.

        If retrieving data fails, the method should throw GetDataFailed exception.

        The exception is not allowed to contain any data except the name of
        the storage class.
        """
        pass

    @abstractmethod
    def set_data(self, user, data):
        """
        Set data for user to storage.

        If the specified user is invalid, the method should throw InvalidUser exception.

        If setting data fails, the method should throw SetDataFailed exception.

        The exception is not allowed to contain any data except the name of
        the storage class.
        """
        pass
