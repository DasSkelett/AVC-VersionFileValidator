import json
import logging as log
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

    log.info(f'Ignoring {[str(f) for f in ignored_files]}')

    if not version_files:
        log.warning('No version files found.')
        return 0, successful_files, failed_files, ignored_files

    log.info(f'Found {[str(f) for f in version_files]}')
    schema = get_schema()
    if not schema:
        return 1, successful_files, failed_files, ignored_files

    for f in version_files:
        try:
            # The actual validation happens here.
            check_single_file(f, schema)
        except json.decoder.JSONDecodeError as e:
            log.error(f'Failed loading {str(f)} as JSON. Check for syntax errors around the mentioned line: {e}')
            failed_files.add(f)
            continue
        except jsonschema.ValidationError as e:
            log.error(f'Validation of {f} failed: {e}')
            failed_files.add(f)
            continue

        successful_files.add(f)

    log.debug('Done!')
    if failed_files:
        log.error(f'The following files failed validation: {[str(f) for f in failed_files]}')
        return 1, successful_files, failed_files, ignored_files
    else:
        return 0, successful_files, failed_files, ignored_files


def calculate_all_exclusions(exclude: str) -> Set[Path]:
    all_exclusions = set()
    if exclude and not exclude.isspace():
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
    log.debug('Fetching schema...')
    try:
        return requests.get(
            'https://raw.githubusercontent.com/linuxgurugamer/KSPAddonVersionChecker/master/KSP-AVC.schema.json'
        ).json()
    except ValueError:
        log.error('Current schema not valid JSON, that\'s unfortunate...')
        return None


def check_single_file(f: Path, schema):
    log.debug(f'Loading {f}')
    with f.open('r') as vf:
        json_file = json.load(vf)
    log.debug(f'Validating {f}')
    jsonschema.validate(json_file, schema)

    # Check URL property ("Location of a remote version file for update checking")
    vf_url = json_file.get('URL')
    if vf_url:
        try:
            remote = json.loads(requests.get(vf_url).content)
            jsonschema.validate(remote, schema)
        except requests.exceptions.RequestException as e:
            log.error(f'Failed downloading remote version file at {vf_url}. Note that the URL property, when used, \n'
                      'must point to the "Location of a remote version file for update checking":')
            raise e
        except json.decoder.JSONDecodeError as e:
            log.error(f'Failed loading remote version file at {vf_url}. Note that the URL property, when used, \n'
                      'must point to the "Location of a remote version file for update checking":')
            raise e
        except jsonschema.ValidationError as e:
            log.error(f'Validation failed for remote version file at {vf_url}. Note that the URL property, when used, \n'
                      'must point to the "Location of a remote version file for update checking":')
            raise e

    log.info(f'Validation of {str(f)} successful.')
