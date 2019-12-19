import json
import os
from pathlib import Path
from typing import Set

import jsonschema
import requests


# Returns (status, successful, failed, ignored)
def validate(exclude) -> (int, Set[Path], Set[Path], Set[Path]):

    all_exclusions = calculate_all_exclusions(exclude)

    # GH will set the cwd of the container to the so-called workspace, which is a clone of the triggering repo,
    # assuming the user remembered to add the 'actions/checkout' step before.
    found_files = {f for f in Path().rglob('*')
                   if f.is_file() and f.suffix.lower() == '.version'}

    version_files = found_files.difference(all_exclusions)
    successful_files = set()
    failed_files = set()
    ignored_files = found_files.intersection(all_exclusions)

    print(f'\nIgnoring {[str(f) for f in ignored_files]}')

    if not version_files:
        print('No version files found.')
        return 0, successful_files, failed_files, ignored_files

    print(f'Found {[str(f) for f in version_files]}')
    schema = get_schema()
    if not schema:
        return 1, successful_files, failed_files, ignored_files

    for f in version_files:
        try:
            # The actual validation happens here.
            check_single_file(f, schema)
        except json.decoder.JSONDecodeError as e:
            print('Failed loading JSON file. Check for syntax errors around the mentioned line:')
            print(e)
            failed_files.add(f)
            continue
        except jsonschema.ValidationError as e:
            print('Validation failed:')
            print(e)
            failed_files.add(f)
            continue

        successful_files.add(f)
        print('Validation successful')

    print('Done!')
    if failed_files:
        print('\nThe following files failed validation:')
        print([str(f) for f in failed_files])
        return 1, successful_files, failed_files, ignored_files
    else:
        return 0, successful_files, failed_files, ignored_files


def calculate_all_exclusions(exclude: str) -> Set[Path]:
    all_exclusions = set()
    if exclude:
        try:
            globs = json.loads(exclude)
        except json.decoder.JSONDecodeError:
            # Not a valid JSON array, assume it is a single exclusion glob
            globs = [exclude]

        # If someone passes a string like this: '"./*.version"'
        if isinstance(globs, str):
            globs = [globs]

        for _glob in globs:
            all_exclusions = all_exclusions.union(Path().glob(_glob))
    return all_exclusions


def get_schema():
    print('Fetching schema...')
    try:
        return requests.get(
            'https://raw.githubusercontent.com/linuxgurugamer/KSPAddonVersionChecker/master/KSP-AVC.schema.json'
        ).json()
    except ValueError:
        print('Current schema not valid JSON, that\'s unfortunate...')
        return None


def check_single_file(f: Path, schema):
    print(f'\nLoading {f}')
    with f.open('r') as vf:
        json_file = json.load(vf)
    print(f'Validating {f}')
    jsonschema.validate(json_file, schema)


if __name__ == "__main__":
    EXCLUDE = os.getenv('INPUT_EXCLUDE')

    (status, successful, failed, ignored) = validate(EXCLUDE)
    print(f'Exiting with status {status}, {len(successful)} successful, {len(failed)} failed, {len(ignored)} ignored.')
    exit(status)
