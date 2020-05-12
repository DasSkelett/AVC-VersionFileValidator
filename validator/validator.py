import json
import logging as log
from pathlib import Path
from typing import Set

import jsonschema
import requests

from .ksp_version import KspVersion
from .versionfile import VersionFile


def validate_cwd(exclude, schema=None, build_map=None):
    """Validates recursively the version files found in the current working directory.

    :param exclude: A string formatted as JSON array containing files or directories to exclude. Supports wildcards.
    :param schema: A **valid** Python object representing the schema. Use sparingly, intended for tests!
    :param build_map: A **valid** Python object representing the build map. Use sparingly, intended for tests!
    :return: A 4-tuple containing the validation status, valid files, failed files and ignored files.
    :rtype: (int, Set[Path], Set[Path], Set[Path])
    """
    all_exclusions = calculate_all_exclusions(exclude)

    # GH will set the cwd of the container to the so-called workspace, which is a clone of the triggering repo,
    # assuming the user remembered to add the 'actions/checkout' step before.
    found_files = {f for f in Path().rglob('*')
                   if f.is_file() and f.suffix.lower() == '.version'}

    version_files = found_files.difference(all_exclusions)
    ignored_files = found_files.intersection(all_exclusions)

    if ignored_files:
        log.info(f'Ignoring {[str(f) for f in ignored_files]}')

    (code, successful_files, failed_files) = check_file_set(version_files, schema, build_map)
    return code, successful_files, failed_files, ignored_files


def validate_list(file_list, schema=None, build_map=None):
    """Validates all the given files in the list.

    :param file_list: A list of strings that are relative or absolute paths to the files that should be validated.
    :param schema: A **valid** Python object representing the schema. Use sparingly, intended for tests!
    :param build_map: A **valid** Python object representing the build map. Use sparingly, intended for tests!
    :return: A 4-tuple containing the validation status, valid files, failed files and ignored files.
    :rtype: (int, Set[Path], Set[Path], Set[Path])
    """
    version_files = set()
    nonexistent_files = set()
    for f in file_list:
        p = Path(f)
        if p and p.is_file():
            version_files.add(p)
        else:
            nonexistent_files.add(f)

    if nonexistent_files:
        log.info(f'Files {[str(f) for f in nonexistent_files]} don\'t exist')

    (code, successful_files, failed_files) = check_file_set(version_files, schema, build_map)
    return code, successful_files, failed_files, nonexistent_files


def check_file_set(version_files, schema=None, build_map=None):
    """Validates the given set of files.

    :param version_files: A set of Path-es to validate.
    :param schema: A **valid** Python object representing the schema. Use sparingly, intended for tests!
    :param build_map: A **valid** Python object representing the build map. Use sparingly, intended for tests!
    :return: A 4-tuple containing the validation status, valid files and failed files.
    :rtype: (int, Set[Path], Set[Path])
    """
    successful_files = set()
    failed_files = set()

    if not version_files:
        log.warning('No version files found.')
        return 0, successful_files, failed_files

    log.info(f'Found {[str(f) for f in version_files]}')

    if schema is None:
        schema = get_schema()
    if schema is None:
        return 1, successful_files, failed_files
    if build_map is None:
        build_map = get_build_map()

    latest_ksp = None
    if build_map is not None:
        builds = build_map.get('builds', None)
        if builds is not None:
            latest_ksp = KspVersion(list(builds.values())[-1])

    for f in version_files:
        # The actual validation happens here.
        valid = check_single_file(f, schema, latest_ksp)
        if valid:
            successful_files.add(f)
        else:
            failed_files.add(f)

    log.debug('Done!')
    if failed_files:
        log.error(f'The following files failed validation: {[str(f) for f in failed_files]}')
        return 1, successful_files, failed_files
    else:
        return 0, successful_files, failed_files


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
            'https://github.com/linuxgurugamer/KSPAddonVersionChecker/raw/master/KSP-AVC.schema.json'
        ).json()
    except ValueError:
        log.error('Current schema not valid JSON, that\'s unfortunate...')
        return None


def get_build_map():
    log.debug('Fetching build map...')
    try:
        return requests.get('https://github.com/KSP-CKAN/CKAN-meta/raw/master/builds.json').json()
    except requests.exceptions.RequestException:
        log.debug('Failed downloading build map from the CKAN-meta repository.')
    except ValueError:
        log.debug('Current build map is not valid JSON, that\'s unfortunate...')
    return None


# Returns a bool to indicate whether the file and its remote is valid or not.
def check_single_file(f: Path, schema, latest_ksp):
    try:
        log.info(f'Checking {f}')
        with f.open('r') as vf:
            log.debug(f'Loading {f}')
            version_file = VersionFile(vf.read())

        log.debug(f'Validating {f}')
        version_file.validate(schema, False)
        if latest_ksp is not None and not version_file.is_compatible_with_ksp(latest_ksp):
            log.warning(f"The file {f} doesn't indicate compatibility "
                        f"with the latest version of KSP ({str(latest_ksp)}). "
                        f"Did you forget to update it?")

        # Check remote version file
        try:
            log.info(f'Checking remote of {f}')
            if remote := version_file.get_remote():
                remote.validate(schema)
                try:
                    if latest_ksp is not None and not remote.is_compatible_with_ksp(latest_ksp):
                        log.warning(f"The remote version file of {f} doesn't indicate compatibility "
                                    f"with the latest version of KSP ({str(latest_ksp)}). "
                                    f"Did you forget to update it? {version_file.url}")
                except:
                    pass

        except requests.exceptions.RequestException:
            log.warning(f'Failed downloading remote version file at {version_file.url}. '
                      'Note that the URL property, when used, '
                      'must point to the "Location of a remote version file for update checking"')
        except json.decoder.JSONDecodeError as e:
            log.warning(f'Failed loading remote version file at {version_file.url}. '
                      f'Note that the URL property, when used, '
                      f'must point to the "Location of a remote version file for update checking". '
                      f'Check for a syntax error around the mentioned line: {e}')
        except jsonschema.ValidationError as e:
            log.warning(f'Validation failed for remote version file at {version_file.url}. '
                      f'Note that the URL property, when used, '
                      f'must point to the "Location of a remote version file for update checking": {e}')

    except json.decoder.JSONDecodeError as e:
        log.error(f'Failed loading {f} as JSON. Check for syntax errors around the mentioned line: {e}')
        return False

    except jsonschema.ValidationError as e:
        log.error(f'Validation of {f} failed: {e}')
        return False

    log.debug(f'Validation of {f} successful.')
    return True
