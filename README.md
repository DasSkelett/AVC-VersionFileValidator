# KSP-AVC Version File Validator

![Unit Tests](https://github.com/DasSkelett/AVC-VersionFileValidator/workflows/Run%20unit%20tests/badge.svg) ![Full Integration Test](https://github.com/DasSkelett/AVC-VersionFileValidator/workflows/Test%20full%20integration/badge.svg)

This repository hosts a Docker-based GitHub Action written in Python3.8 that you can use in a workflow in your [KSP](https://www.kerbalspaceprogram.com/) mod repo.
It will validate all [KSP-AVC](https://github.com/linuxgurugamer/KSPAddonVersionChecker) version files in the repository against [the official KSP-AVC schema](https://github.com/linuxgurugamer/KSPAddonVersionChecker/blob/master/KSP-AVC.schema.json).

This is intended for authors and maintainers of [Kerbal Space Program](https://www.kerbalspaceprogram.com/) mods.

No more missing commas that prevent your latest release from being indexed by the CKAN.

## Usage
### In a GitHub workflow (default)
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
Make sure workflows are activated in your repository settings:
![workflow settings](https://user-images.githubusercontent.com/28812678/73135906-291fe300-4048-11ea-992a-3a0a3800c730.png)
The top radio button should be selected.

To exclude files, add a JSON array containing the paths to the files (relative from repo rooot) as `exclude` parameter after `- name: Validate files`:
```yaml
        with:
          exclude: '["./invalid.version", "./test/corruptVersionFiles/**/*.version"]'
```
You can also use globbing statements, for the syntax see syntax, see the [pathlib documentation](https://docs.python.org/3.5/library/pathlib.html#pathlib.PurePath.match).

**For more workflow file examples, see the [examples folder](https://github.com/DasSkelett/AVC-VersionFileValidator/tree/master/examples).**

### Use the package outside of a GitHub action, like Travis
You need Python 3.8 installed! Setup:
```sh
git clone https://github.com/DasSkelett/AVC-VersionFileValidator.git
cd AVC-VersionFileValidator
python3.8 -m venv venv
source venv/bin/activate
pip install --user -r requirements.txt
```
Now use the validator. It is important that your current working directory is the directory where the version files you want to test are located! 
Also make sure you have the venv activated!
```
cd ../<YourMod>
python ../AVC-VersionFileValidator/main.py
```

Furthermore, if you use an IDE that supports custom JSON schemas, I strongly recommend using this feature.

## Development
### Set up development environment
I recommend setting up a virtual environment, especially if you are using an IDE:
```sh
python3.8 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

The Action itself is a Docker image/container (requirement by GitHub). You can use the same Dockerfile for running it locally,
but remember to set the right environment variables if needed .

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
If you want to run the unit tests on your host, do the following (remember venv!):
```sh
python -m unittest tests
```
Note that the test framework assumes that your current working directory is this project's root.
