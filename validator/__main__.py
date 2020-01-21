import os
from distutils.util import strtobool

from validator import validate
from utils import setup_logger


def validate_current_repository():
    debug = bool(strtobool(os.getenv('INPUT_DEBUG', 'false')))
    setup_logger(debug)

    exclude = os.getenv('INPUT_EXCLUDE', '')

    (status, successful, failed, ignored) = validate(exclude)
    print(f'Exiting with status {status}, {len(successful)} successful, {len(failed)} failed, {len(ignored)} ignored.')
    exit(status)


if __name__ == "__main__":
    validate_current_repository()
