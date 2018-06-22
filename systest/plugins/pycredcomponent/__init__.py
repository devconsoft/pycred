from k2.config.options import ConfigOptionId
from k2.config.types import Path, Flag

COVERAGE_ENABLED = ConfigOptionId(
    'coverage.enabled', 'Enables coverage measurement', option_type=Flag(), default=False)

COVERAGE_CONFIG_FILE = ConfigOptionId(
    'coverage.config.file',
    'Specifies a config file that will be forwarded to coverage',
    option_type=Path(exists=True))
