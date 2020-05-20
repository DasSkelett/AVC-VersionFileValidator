import re
from functools import total_ordering


@total_ordering
class KspVersion:
    rgx = re.compile('^(?P<major>\d+)\.(?P<minor>\d+)(\.(?P<patch>\d+))?(\.(?P<build>\d+))?$')

    @classmethod
    def try_parse(cls, version):
        try:
            return KspVersion(version)
        except:
            return None

    def __init__(self, version):
        # Assume it's either 'any' or a semantic version according to the schema.
        if isinstance(version, str):
            if version == 'any':
                self.any = True
                return
            else:
                self.any = False
                match = self.rgx.fullmatch(version)
                self.major = int(match.group('major'))
                self.minor = int(match.group('minor'))
                self.patch = int(m) if (m := match.group('patch')) is not None else None
                self.build = int(m) if (m := match.group('build')) is not None else None

        elif isinstance(version, dict):
            self.any = False
            self.major = int(version.get('MAJOR'))
            self.minor = int(version.get('MINOR'))
            self.patch = int(m) if (m := version.get('PATCH')) is not None else None
            self.build = int(m) if (m := version.get('BUILD')) is not None else None
        else:
            raise TypeError('The version is neither a well-formatted string nor a dict.')
        if not (self.major and self.minor):
            raise TypeError('Version needs at least a MAJOR and MINOR.')

    # From AVC code:
    # (Ignoring KSP_INCLUDE_VERSIONS and KSP_EXCLUDE_VERSIONS)
    # If no ksp_version_min and no ksp_version_max are defined, return whether compatible with ksp_version
    # If at least one of _min or _max is defined, return whether it matches those two.
    # That means, ksp_version is ignored when _min and/or _max are defined.
    # https://github.com/linuxgurugamer/KSPAddonVersionChecker/blob/90ca9738da412f31a95a29209784ad48e8d082c4/KSP-AVC/AddonInfo.cs#L149-L165
    # This is neat, because CKAN handles that pretty similar.
    def is_contained_in(self, ksp_version, ksp_version_min, ksp_version_max):
        if self.any or getattr(ksp_version, 'any', False) \
                or getattr(ksp_version_min, 'any', False) or getattr(ksp_version_max, 'any', False):
            return True
        if ksp_version_min and ksp_version_max:
            return ksp_version_min <= self <= ksp_version_max
        if ksp_version_min and not ksp_version_max:
            return ksp_version_min <= self
        if ksp_version_max and not ksp_version_min:
            return self <= ksp_version_max
        # Else no _min or _max
        if ksp_version:
            return self == ksp_version
        return False

    def fully_equals(self, other):
        if self.any != other.any:
            return False
        if self.major != other.major:
            return False
        if self.minor != other.minor:
            return False
        if self.patch != other.patch:
            return False
        if self.build != other.build:
            return False
        return True

    def __eq__(self, other):
        return not self > other and not other > self

    def __gt__(self, other):
        # Thanks to the  regex we can assume everything is a int.
        # We can also assume major and minor exist.
        # One specialty: a.b is always equal to a.b.c and a.b.c.d
        if self.major > other.major:
            return True
        elif self.major < other.major:
            return False
        if self.minor > other.minor:
            return True
        elif self.minor < other.minor:
            return False
        if self.patch and other.patch:
            if self.patch > other.patch:
                return True
            elif self.patch < other.patch:
                return False
        else:
            return False
        if self.build and other.build:
            if self.build > other.build:
                return True
            elif self.build < other.build:
                return False
            elif self.build == other.build:
                return False
        else:
            return False

    def __str__(self):
        string = '' + str(self.major)
        string = string + '.' + str(self.minor)
        string = string + '.' + str(self.patch) if self.patch else string
        string = string + '.' + str(self.build) if self.build else string
        return string
