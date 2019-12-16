import fnmatch
import json
import os
import re
from pathlib import Path

import jsonschema
import requests


def main():
    GH_WORKSPACE = os.getenv('GITHUB_WORKSPACE')
    EXCLUDE = os.getenv('INPUT_EXCLUDE')

    if not GH_WORKSPACE:
        print('Error! Missing $GITHUB_WORKSPACE')
        exit(1)

    os.chdir(Path(os.getcwd(), GH_WORKSPACE))

    if EXCLUDE:
        exclude_files = [Path(f) for f in EXCLUDE.split(',')]
    else:
        exclude_files = []

    version_files = (f for f in Path('.').rglob('*')
                     if f.is_file() and f not in exclude_files and f.suffix.lower() == '.version')

    # How to lazy-get this only when version_files is not empty (which is a generator)?
    schema = get_schema()

    for f in version_files:
        with f.open('r') as vf:
            try:
                print(f'Loading {f}')
                json_file = json.load(vf)
            except json.decoder.JSONDecodeError as e:
                print('Failed loading JSON file. Check for syntax errors around the mentioned line:')
                print(e.msg)
                exit(1)

        try:
            print(f'Validating {f}')
            jsonschema.validate(json_file, schema)
        except jsonschema.ValidationError as e:
            print('Validation failed, see message below:')
            print(e.message)
            exit(1)

    print('Done!')
    exit(0)


def get_schema():
    try:
        return requests.get(
            'https://raw.githubusercontent.com/linuxgurugamer/KSPAddonVersionChecker/master/KSP-AVC.schema.json'
        ).json()
    except ValueError:
        print('Current schema not valid JSON, that\'s unfortunate...')
        exit(1)


if __name__ == "__main__":
    main()
