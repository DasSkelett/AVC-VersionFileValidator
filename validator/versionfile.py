import json
import logging as log
import re
from pathlib import Path

import jsonschema
import requests

from .ksp_version import KspVersion


class VersionFile:

    def __init__(self, content: str, path: Path):

        self.json = json.loads(content)
        self.raw = content

        self.name = self.json.get('NAME')
        self.url = self.json.get('URL')
        self.download = self.json.get('DOWNLOAD')
        self.changelog = self.json.get('CHANGE_LOG')
        self.changelog_url = self.json.get('CHANGE_LOG_URL')

        if gh := self.json.get('GITHUB'):
            self.github = True
            self.github_username = gh.get('USERNAME')
            self.github_repository = gh.get('REPOSITORY')
            self.github_allow_prerelease = gh.get('ALLOW_PRE_RELEASE')

        self.disallow_version_override = self.json.get('DISALLOW_VERSION_OVERRIDE')
        self.kerbalstuff_url = self.json.get('KERBAL_STUFF_URL')
        self.assembly_name = self.json.get('ASSEMBLY_NAME')
        self.ksp_version_include = self.json.get('KSP_VERSION_INCLUDE')
        self.ksp_version_include = self.json.get('KSP_VERSION_INCLUDE')
        self.ksp_version_exclude = self.json.get('KSP_VERSION_EXCLUDE')
        self.local_has_priority = self.json.get('LOCAL_HAS_PRIORITY')
        self.remote_has_priority = self.json.get('REMOTE_HAS_PRIORITY')

        self.version = self.json.get('VERSION')

        self.ksp_version = KspVersion.try_parse(v) if (v := self.json.get('KSP_VERSION')) is not None else None
        self.ksp_version_min = KspVersion.try_parse(v) if (v := self.json.get('KSP_VERSION_MIN')) is not None else None
        self.ksp_version_max = KspVersion.try_parse(v) if (v := self.json.get('KSP_VERSION_MAX')) is not None else None

        # I doubt we will ever have to deal with it, so we don't care about INSTALL_LOC* for now.

        self._remote = None
        self.valid = False
        self.path = path

    def get_remote(self):
        if self._remote:
            return self._remote
        if not self.url:
            return None
        log.debug('Fetching remote...')
        response = requests.get(get_raw_uri(self.url))
        response.raise_for_status()
        self._remote = VersionFile(response.text, self.path)
        return self._remote

    # Validates this and optional a remote version file. Throws all exception it encounters.
    def validate(self, schema: dict, validate_remote=False):
        self.valid = False
        jsonschema.validate(self.json, schema)

        if not validate_remote:
            self.valid = True
            return

        remote = self.get_remote()
        remote.validate(schema, False)
        # No exceptions -> True
        self.valid = True

    def is_compatible_with_ksp(self, version: KspVersion) -> bool:
        if version is None:
            return False
        return version.is_contained_in(self.ksp_version, self.ksp_version_min, self.ksp_version_max)


def get_raw_uri(uri: str) -> str:
    # Returns (scheme, netloc, path, params, query, fragment) with the rule:
    # <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
    parts = requests.utils.urlparse(uri)
    if parts.netloc != 'github.com':
        return uri

    # Do a bit of a dance. We don't want to replace 'tree' or 'blob' if it's part of a filename.
    # AVC doesn't pay attention to this, it replaces all occurrences of those two keys wherever they are,
    # and potentially destroys URLs this way.
    path_regex = re.compile(
        '^/(?P<user>[^/]+)/(?P<repo>[^/]+)/(?P<key>(blob|tree))/(?P<branch>[^/]+)/(?P<path>.+)$'
    )

    repl = r'/\g<user>/\g<repo>/raw/\g<branch>/\g<path>'
    path_subst = re.sub(pattern=path_regex, repl=repl, string=parts.path)
    if '/blob/' in path_subst or '/tree/' in path_subst:
        log.warning("Don't put version files in paths containing 'blob' or 'tree', AVC will break the URL.")

    new_parts = (parts.scheme, parts.netloc, path_subst, parts.params, parts.query, parts.fragment)
    return requests.utils.urlunparse(new_parts)
