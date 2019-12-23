# KSP-AVC Version File Validator

This repository hosts a Docker-based GitHub Action written in Python3 that you can use in a workflow in your [KSP](https://www.kerbalspaceprogram.com/) mod repo.
It will validate all [KSP-AVC](https://github.com/linuxgurugamer/KSPAddonVersionChecker) version files in the repository against [the official KSP-AVC schema](https://github.com/linuxgurugamer/KSPAddonVersionChecker/blob/master/KSP-AVC.schema.json).

This is intended for authors and maintainers of [Kerbal Space Program](https://www.kerbalspaceprogram.com/) mods.

No more missing commas that prevent your latest release from being indexed by the CKAN.

## Usage
### As GitHub Action in a workflow (default)
Download the [standard workflow file](https://github.com/DasSkelett/AVC-VersionFileValidator/blob/master/examples/standard.yml) and save it under `<YourMod>/.github/workflows/AVC-VersionFileValidator.yml`.
Then commit and push it to GitHub.
 
Alternatively, copy the following and put it in `<YourMod>/.github/workflows/AVC-VersionFileValidator.yml`.
```yaml
name: Validate AVC .version files
on:
  push:
  pull_request:
    types: [opened, synchronize, reopened]
jobs:
  validate_version_files:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v2
        with:
          fetch-depth: 1
      - name: Validate files
        uses: DasSkelett/AVC-VersionFileValidator@v1
```
Make sure workflows are activated in your repository settings.

Optionally, add the following after `- name: Validate files` to exclude `invalid.version` and every version file in `test/corruptVersionFiles/` and any subdirectory of it:
```yaml
        with:
          exclude: '["./invalid.version", "./test/corruptVersionFiles/**/*.version"]'
```
The supplied string has to be a valid JSON array (except it's a single file or globbing statement, then it can be a simple string)!
For the globbing syntax, see the [pathlib documentation](https://docs.python.org/3.5/library/pathlib.html#pathlib.PurePath.match).

**For more workflow file examples, see the [examples folder](https://github.com/DasSkelett/AVC-VersionFileValidator/tree/master/examples).**

### Validate single .version file once on your PC
If you simply want to check the version file once locally, you don't have to use this action, just run:
```sh
wget https://raw.githubusercontent.com/linuxgurugamer/KSPAddonVersionChecker/master/KSP-AVC.schema.json
pip3 install --user jsonschema
python3 -m jsonschema -i YourMod.version KSP-AVC.schema.json
```
Is you use an IDEs that supports custom JSON schemas, I strongly recommend using it.

### Validate multiple .version files once on your PC
If you want to check an entire local directory with potentially multiple version files, use this action as standard Python application:
```sh
git clone https://github.com/DasSkelett/AVC-VersionFileValidator.git
cd AVC-VersionFileValidator
pip3 install --user -r requirements.txt
# It is important that your current working directory is the directory where the version files you want to test are located!  
cd ../<YourMod>
python3 ../AVC-VersionFileValidator/validator/main.py
```

## Development
## Set up development environment
I recommend setting up a virtual environment, especially if you are using an IDE:
```sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

The Action itself is a Docker image/container (requirement by GitHub). You can use the same Dockerfile for running it locally,
but remember to set the right environment variables if needed 

The repository is set up in a way that supports running the app directly or in a Docker container.
Same goes for the tests. You only have to pay attention what your current working directory is when you invoke Python!  

### Testing
This project uses `unittest`, which is part of the Python stdlib.

#### Run tests in Docker Container
If you want to run the unit tests using Docker:
```sh
docker build --target tests -t avc-versionfilevalidator . && docker run avc-versionfilevalidator
```

#### Without Docker Container
If you want to run the unit tests on your host, do the following.
```sh
python3 -m unittest tests/main.py
```
Note that the test framework assumes that your current working directory is this project's root.

## TODO
* Make GitHub build Dockerfile default stage only (currently also executes the steps in the `tests` stage, which is unnecessary)
* Option to only check specific version files (should ignore exclusion)
* Better logging output

## This Action is based on instructions to create a Docker GitHub Action found here:

> https://github.blog/2019-06-06-generate-new-repositories-with-repository-templates/.
>
> https://github.com/actions/toolkit/blob/master/docs/container-action.md
>
> https://help.github.com/en/actions/automating-your-workflow-with-github-actions/building-actions
