import logging
import subprocess

from k2.cmd.run import RUN_COMMAND
from k2.config.options import ConfigOption
from k2.component.decorator import component
from k2.extensions.extension import CommandExtension, AbstractExtension, get_logger_name

from . import COVERAGE_ENABLED, COVERAGE_CONFIG_FILE

logger = logging.getLogger(get_logger_name('pycredcomponent'))
logger.addHandler(logging.NullHandler())


@CommandExtension(
    'pycredcomponent',
    extends=[RUN_COMMAND],
    config_options=[
        ConfigOption(COVERAGE_CONFIG_FILE, required=False),
        ConfigOption(COVERAGE_ENABLED, required=False),
    ])
class PyCredExtension(AbstractExtension):

    def __init__(self, config, instances):

        @component()
        class PyCred(object):

            coverage_enabled = config.get(COVERAGE_ENABLED, False)
            coverage_config_file = config.get(COVERAGE_CONFIG_FILE)

            def __init__(self, command, expected_exit_code=0):

                if PyCred.coverage_enabled:
                    config_file_arg = ''
                    if PyCred.coverage_config_file:
                        config_file_arg = '--rcfile {file}'.format(file=PyCred.coverage_config_file)

                    prefix = "coverage run {config_file_arg} --parallel-mode".format(
                        config_file_arg=config_file_arg)
                else:
                    prefix = ''

                pycred_entry_point = subprocess.check_output(
                    ['which', 'pycred'], universal_newlines=True).strip()

                pycred_command = (
                    "{prefix} "
                    "{entry_point} "
                    "{command}").format(
                        prefix=prefix,
                        entry_point=pycred_entry_point,
                        command=command)

                logger.info('Running pycred command: {command}'.format(command=pycred_command))
                self.result = subprocess.Popen(
                    pycred_command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True)
                self.result.wait(timeout=10)
                self.stdout = self.result.stdout.read()
                self.stderr = self.result.stderr.read()
                logger.debug('-------- stdout --------')
                for line in self.stdout.split('\n'):
                    logger.debug(line)
                logger.debug('-------- end stdout --------')
                logger.debug('-------- stderr --------')
                for line in self.stderr.split('\n'):
                    logger.debug(line)
                logger.debug('-------- end stderr --------')

                if self.result.returncode != expected_exit_code:
                    raise AssertionError(self.stderr)
