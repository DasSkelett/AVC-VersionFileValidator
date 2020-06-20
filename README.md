# KSP-AVC Version File Validator

![Unit Tests](https://github.com/DasSkelett/AVC-VersionFileValidator/workflows/Unit%20Tests/badge.svg) ![Full Integration Test](https://github.com/DasSkelett/AVC-VersionFileValidator/workflows/Full%20Integration%20Test/badge.svg) ![Full Integration Test (Docker)](https://github.com/DasSkelett/AVC-VersionFileValidator/workflows/Full%20Integration%20Test%20(Docker)/badge.svg)

[This repository](https://github.com/DasSkelett/AVC-VersionFileValidator) hosts a Docker-based GitHub Action written in Python3.8 that you can use in a workflow in your [KSP](https://www.kerbalspaceprogram.com/) mod repo.
It will validate all [KSP-AVC](https://github.com/linuxgurugamer/KSPAddonVersionChecker) version files in the repository against [the official KSP-AVC schema](https://github.com/linuxgurugamer/KSPAddonVersionChecker/blob/master/KSP-AVC.schema.json).

This is intended for authors and maintainers of [Kerbal Space Program](https://www.kerbalspaceprogram.com/) mods.

No more missing commas that prevent your latest release from being indexed by the CKAN.

## Usage
### In a GitHub workflow (default)
Download the [standard workflow file](https://github.com/DasSkelett/AVC-VersionFileValidator/blob/master/examples/standard.yml) and save it under `<YourMod>/.github/workflows/AVC-VersionFileValidator.yml`.
Then commit and push it to GitHub.
 
Alternatively, copy the following and put it in `<YourMod>/.github/workflows/AVC-VersionFileValidator.yml`.
```yaml
name: AVC .version file validation
on:
  push:
    branches:
      - master
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
        uses: DasSkelett/AVC-VersionFileValidator
```
Make sure workflows are activated in your repository settings:
![workflow settings](https://user-images.githubusercontent.com/28812678/73135906-291fe300-4048-11ea-992a-3a0a3800c730.png)
The top radio button should be selected.

#### Parameters
Workflow files support passing parameters to the executed Actions using the `with` property,
The following options are available for the KSP-AVC Version File Validator:

##### Blacklist / Exclusions
To exclude files, add a JSON array containing the paths to the files (relative from repo root) as `exclude` parameter after `- name: Validate files`:
```yaml
        with:
          exclude: '["./GameData/BundledMod/BundledMod.version", "./GameData/OtherBundledMod/**/*.version"]'
```
You can use globbing statements, for the syntax see the [pathlib documentation](https://docs.python.org/3.5/library/pathlib.html#pathlib.PurePath.match).

[Example](https://github.com/DasSkelett/AVC-VersionFileValidator/tree/master/examples/exclusions.yml)

##### Whitelist / Inclusions
If you only want to test a specific set of files, you can use the `only` parameter. Can't be used together with `exclude`!
```yaml
        with:
          only: '["./GameData/YourMod/YourMod.version"]'
```

[Example](https://github.com/DasSkelett/AVC-VersionFileValidator/tree/master/examples/whitelist.yml)


### Outside of a GitHub action, like locally or in Travis
You need Python 3.8 installed! Setup:
```sh
git clone https://github.com/DasSkelett/AVC-VersionFileValidator.git
cd AVC-VersionFileValidator
python3.8 -m venv venv
source venv/bin/activate
pip install --upgrade -r requirements.txt
```
Now use the validator. Make sure you have the venv activated!
```sh
python main.py ../<YourMod>/GameData/<YourMod>/<YourMod>.version
```
Alternatively, if there are more version files to be checked, switch your working directory to the root of your repo and execute main.py from there.
It will search for version files recursively.
```sh
cd ../<YourMod>
python ../AVC-VersionFileValidator/main.py
```

Furthermore, if you use an IDE that supports custom JSON schemas, I strongly recommend using this feature.

## Development
### Setup development environment
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
