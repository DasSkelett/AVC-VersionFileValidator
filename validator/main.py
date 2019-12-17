import json
import os
from pathlib import Path

import jsonschema
import requests


def validate(exclude):
    if exclude:
        exclude_files = [Path(f) for f in exclude.split(',')]
    else:
        exclude_files = []

    # GH will set the cwd of the container to the so-called workspace, which is a clone of the triggering repo,
    # assuming the user remembered to add the 'actions/checkout' step before.
    version_files = (f for f in Path('.').rglob('*')
                     if f.is_file() and f not in exclude_files and f.suffix.lower() == '.version')

    # How to lazy-get this only when version_files is not empty (which is a generator)?
    schema = get_schema()

    failed_files = []

    for f in version_files:
        print(f'\nLoading {f}')
        try:
            with f.open('r') as vf:
                json_file = json.load(vf)
        except json.decoder.JSONDecodeError as e:
            print('Failed loading JSON file. Check for syntax errors around the mentioned line:')
            print(e)
            failed_files.append(f.name)
            continue

        print(f'Validating {f}')
        try:
            jsonschema.validate(json_file, schema)
        except jsonschema.ValidationError as e:
            print('Validation failed:')
            print(e)
            failed_files.append(f.name)
            continue
        print('Validation successful')

    print('Done!')
    if failed_files:
        print('\nThe following files failed validation:')
        print(failed_files)
        return 1
    else:
        return 0


def get_schema():
    print('Fetching schema...')
    try:
        return requests.get(
            'https://raw.githubusercontent.com/linuxgurugamer/KSPAddonVersionChecker/master/KSP-AVC.schema.json'
        ).json()
    except ValueError:
        print('Current schema not valid JSON, that\'s unfortunate...')
        exit(1)


if __name__ == "__main__":
    EXCLUDE = os.getenv('INPUT_EXCLUDE')

    exit(validate(EXCLUDE))
