# This file contains all notable changes to the AVC-VersionFileValidator

## master (not included in any release yet)
* Validate remote version file if specified with `URL` property.
* Make the validator importable as a package (#4 by: DasSkelett)
* Use logging instead of print(), make use of the Action logging syntax (#4 by: DasSkelett)
* Implement KSP version comparison logic + warn for outdated KSP compatibilities (#5 by: DasSkelett)


## v1
### v1.1.1
* Add requirements.txt for easier dev env setup.
* Add examples in the examples/ folder. The standard.yml should cover most use cases.
* Do not overwrite requirements.txt if it exists in the triggering repo.

### v1.1.0
* Allow wildcards in the exclusion input arguments. They are evaluated according to Python3's pathlib.Glob() function,
    so recursive exclusions (`**/*.version`) are supported. The exclusion value has to be a JSON array now!
* Output handy details when finishing validation (number of failed, successful, ignored)
* Add CHANGELOG.md
* Push PyCharm IDE settings into repository.
    Includes configurations for running the tests in a container or on the host directly,
    running the validator itself in one of the test workspaces (container or host).
* Unit test setup

### v1.0.0
Initial release.
Supports basic functionality as well as excluding specific files, specified in the input.exclude parameter.
See README.md for usage information.
