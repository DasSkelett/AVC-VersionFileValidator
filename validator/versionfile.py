import json

import jsonschema
import requests

from .ksp_version import KspVersion


class VersionFile:

    def __init__(self, content: str):

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

        # I doubt we will ever have to handle with them, so I don't care about INSTALL_LOC* for now.

        self._remote = None
        self.valid = False

    def get_remote(self):
        if self._remote:
            return self._remote
        if not self.url:
            return None
        self._remote = VersionFile(requests.get(self.url).content)
        return self._remote

    # Validates this and optional a remote version file. Throws all exception it encounters.
    def validate(self, schema, validate_remote=False):
        self.valid = False
        jsonschema.validate(self.json, schema)

        if not validate_remote:
            self.valid = True
            return

        remote = self.get_remote()
        remote.validate(schema, False)
        # No exceptions -> True
        self.valid = True

    def is_compatible_with_ksp(self, version: KspVersion):
        return version.is_contained_in(self.ksp_version, self.ksp_version_min, self.ksp_version_max)
