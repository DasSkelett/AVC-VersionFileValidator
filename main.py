#!/usr/bin/env python3
import os
import sys
from typing import List

from validator.utils import get_env_array, str_to_bool
from validator.logger import setup_logger
from validator.validator import validate_cwd, validate_list


def main():
    if len(sys.argv) > 1:
        # Assume the provided arguments are a list of files to check.
        argv_whitelist = sys.argv[1:]
        validate_list_of_files(argv_whitelist)
    elif env_whitelist := get_env_array('INPUT_ONLY'):
        # We got a whitelist of files to check via env var
        validate_list_of_files(env_whitelist)
    else:
        # Else go the normal route and check everything in the cwd.
        validate_current_repository()


def validate_current_repository():
    debug = str_to_bool(os.getenv('INPUT_DEBUG', 'false'))
    setup_logger(debug)

    exclude = os.getenv('INPUT_EXCLUDE', '')

    (status, successful, failed, ignored) = validate_cwd(exclude)
    print(f'Exiting with status {status}: {len(successful)} successful, {len(failed)} failed, {len(ignored)} ignored.')
    sys.exit(status)


def validate_list_of_files(file_list: List[str]):
    debug = str_to_bool(os.getenv('INPUT_DEBUG', 'false'))
    setup_logger(debug)

    (status, successful, failed, ignored) = validate_list(file_list)

    print(f'Exiting with status {status}: {len(successful)} successful, {len(failed)} failed, {len(ignored)} ignored.')
    sys.exit(status)


if __name__ == "__main__":
    main()
