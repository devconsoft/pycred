from abc import ABCMeta, abstractmethod


class GetDataFailed(Exception):
    """Thrown if data could not be retrieved from storage."""

    def __init__(self, storage):
        super().__init__('Get data failed in {storage}'.format(storage=storage))


class SetDataFailed(Exception):
    """Thrown if data passed to storage could not be stored."""

    def __init__(self, storage):
        super().__init__('Set data failed in {storage}'.format(storage=storage))


class UnsetDataFailed(Exception):
    """Thrown if data for the specified user could not be unset (deleted)."""

    def __init__(self, storage):
        super().__init__('Unset data failed in {storage}'.format(storage=storage))


class InvalidUser(Exception):
    """Thrown if the specified user is invalid."""

    def __init__(self, storage):
        super().__init__('Invalid user in {storage}'.format(storage=storage))


class GetUsersFailed(Exception):
    """Thrown if the list of users could not be retrieved for the storage."""

    def __init__(self, storage):
        super().__init__('Get users failed in {storage}'.format(storage=storage))


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

    @abstractmethod
    def unset_data(self, user):
        """
        Unset (delete) data for user in storage.

        If the specified user is invalid, the method should throw InvalidUser exception.

        If unsetting data fails, the method should throw UnsetDataFailed exception.

        The exception is not allowed to contain any data except the name of
        the storage class.
        """
        pass

    @abstractmethod
    def delete(self):
        """Delete any permanent resources associated with the instance."""
        pass

    @abstractmethod
    def get_users(self):
        """Get list of users that has stored credentials in the storage."""
        pass
