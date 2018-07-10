import logging
import tempfile
from unittest.mock import patch

from k2.cmd.run import RUN_COMMAND
from zaf.component.decorator import component
from zaf.extensions.extension import AbstractExtension, CommandExtension, get_logger_name

logger = logging.getLogger(get_logger_name('k2', 'workspacecomponent'))
logger.addHandler(logging.NullHandler())


@CommandExtension('workspacecomponent', extends=[RUN_COMMAND])
class WorkspaceExtension(AbstractExtension):

    def __init__(self, config, instances):

        @component()
        class Workspace(object):

            def __init__(self):
                self.temp_dir = None
                self.path = None
                self.env = None

            def __enter__(self):
                self.temp_dir = tempfile.TemporaryDirectory(prefix='pycred-')
                self.path = self.temp_dir.__enter__()
                self.env = patch.dict('os.environ', {'PYCRED_STORE_PATH': self.path})
                self.env.__enter__()
                logger.info("Creating workspace {d}".format(d=self.path))
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.env.__exit__(exc_type, exc_val, exc_tb)
                self.temp_dir.__exit__(exc_type, exc_val, exc_tb)
                self.env = None
                self.temp_dir = None
                logger.debug("Destroying workspace {d}".format(d=self.path))
                self.path = None
