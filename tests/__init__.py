from validator.utils import setup_logger
from .default import *
from .ksp_version import *
from .singlefiles import *
from .strangenames import *
from .versionfile import *

# Use logging.getLogger('tests').<lvl>() for logging in the tests.
# This will format the messages so that GitHub can parse them as warnings or errors.
setup_logger(True, 'tests')
