# This file contains all notable changes to the AVC-VersonFileValidator

## master (not included in any release yet)
* Allow wildcards in the exclusion input arguments. They are evaluated according to Python3's pathlib Glob()/Match() functions.
* Output handy details when finishing validation (number of failed, successful, ignored)
* Add CHANGELOG.md
* Push PyCharm IDE settings into repository.
    Includes configurations for running the tests in a container or on the host directly,
    running the validator itself in one of the test workspaces (container or host).
* Unit test setup


## v1
### v1.0.0
Initial release.
Supports basic functionality as well as excluding specific files, specified in the input.exclude parameter.
See README.md for usage information.
