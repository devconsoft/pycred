class StoreAlreadyExists(Exception):

    def __init__(self, name):
        super().__init__('Store {name} already exists.'.format(name=name))


class StoreDoesNotExist(Exception):

    def __init__(self, name):
        super().__init__('Store {name} does not exist.'.format(name=name))
