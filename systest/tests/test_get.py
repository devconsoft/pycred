from unittest.mock import patch
import os
import tempfile


def test_get_long_opt_help(pycred):
    pycred('get --help')


def test_get_short_opt_help(pycred):
    pycred('get -h')
