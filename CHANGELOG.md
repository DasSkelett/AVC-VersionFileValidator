# This file contains all notable changes to the AVC-VersionFileValidator

## master (not included in any release yet)
* Add examples in the examples/ folder. The standard.yml should cover most use cases.
* Add requirements.txt for easier dev env setup.


## v1
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
