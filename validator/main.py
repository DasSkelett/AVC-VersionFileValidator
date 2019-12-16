import fnmatch
import json
import jsonschema
from pathlib import Path
import sys
import re
import requests


def main():
    if len(sys.argv) < 3:
        print('Usage: python3.8 main.py $INPUT_EXCLUDE $GITHUB_WORKSPACE')
        exit(1)

    exclude_files = [Path(f) for f in sys.argv[2]]

    # version_files = (f for f in path.glob('**/*.version'))
    version_file_regex = re.compile(fnmatch.translate('**/*.version'), re.IGNORECASE)
    version_files = (f for f in Path(sys.argv[1]).iterdir()
                     if f.is_fifo() and f not in exclude_files and version_file_regex.fullmatch(f))

    # How to lazy-get this with version_files being a generator?
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
            exit(1)

    print('Done!')
    exit(0)


def get_schema():
    try:
        return requests.get(
            'https://raw.githubusercontent.com/linuxgurugamer/KSPAddonVersionChecker/master/KSP-AVC.schema.json'
        ).json()
    except ValueError:
        print('Current schema not valid JSON, trying embedded schema as fallback...')
        exit(1)


if __name__ == "__main__":
    main()
