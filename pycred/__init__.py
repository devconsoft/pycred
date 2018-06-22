try:
    from .version import __version__
except:
    __version__ = None
__version__ = "0.0.0" if not __version__ else __version__
