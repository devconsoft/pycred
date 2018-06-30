import os


def get_resources_dir():
    systest_dir = os.path.dirname(__file__)
    return os.path.join(systest_dir, 'resources')


def get_data_dir():
    return os.path.join(get_resources_dir(), 'data')


def get_stores_dir():
    return os.path.join(get_resources_dir(), 'stores')
