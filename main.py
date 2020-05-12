#!/usr/bin/env python3.8

import os
import sys
from distutils.util import strtobool

from validator.utils import setup_logger
from validator.validator import validate_cwd, validate_list


def validate_current_repository():
    debug = bool(strtobool(os.getenv('INPUT_DEBUG', 'false')))
    setup_logger(debug)

    exclude = os.getenv('INPUT_EXCLUDE', '')

    (status, successful, failed, ignored) = validate_cwd(exclude)
    print(f'Exiting with status {status}: {len(successful)} successful, {len(failed)} failed, {len(ignored)} ignored.')
    exit(status)


def validate_list_of_files(file_list):
    debug = bool(strtobool(os.getenv('INPUT_DEBUG', 'false')))
    setup_logger(debug)

    (status, successful, failed, ignored) = validate_list(file_list)

    print(f'Exiting with status {status}: {len(successful)} successful, {len(failed)} failed, {len(ignored)} ignored.')
    exit(status)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Assume the provided arguments is a list of files to check.
        file_list = sys.argv[1:]
        validate_list_of_files(file_list)

    validate_current_repository()
