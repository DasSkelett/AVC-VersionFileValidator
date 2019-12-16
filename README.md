# KSP-AVC Version File Validator

## Usage
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
        uses: DasSkelett/AVC-VersionFileValidator@master
```

## Local testing
For local testing, run the container like this:
```sh
export GITHUB_WORKSPACE="./tests/workspaces/default"
export INPUT_EXCLUDE=""
docker build --target dev -t avc-versionfilevalidator . && docker run -e GITHUB_WORKSPACE -e INPUT_EXCLUDE avc-versionfilevalidator
```

## TODO
* Make GitHub use Dockerfile default stage only
* Better logging output


## Notes for myself
The container is run using the following command:
```sh
/usr/bin/docker run \
    --name af96b455d270f4dba34dbc989049259055c0ad_a6c67a \
    --label af96b4 \
    --workdir /github/workspace \
    --rm \
    -e INPUT_EXCLUDE \
    -e HOME \
    -e GITHUB_REF \
    -e GITHUB_SHA \
    -e GITHUB_REPOSITORY \
    -e GITHUB_ACTOR \
    -e GITHUB_WORKFLOW \
    -e GITHUB_HEAD_REF \
    -e GITHUB_BASE_REF \
    -e GITHUB_EVENT_NAME \
    -e GITHUB_WORKSPACE \
    -e GITHUB_ACTION \
    -e GITHUB_EVENT_PATH \
    -e RUNNER_OS \
    -e RUNNER_TOOL_CACHE \
    -e RUNNER_TEMP \
    -e RUNNER_WORKSPACE \
    -e ACTIONS_RUNTIME_URL \
    -e ACTIONS_RUNTIME_TOKEN \
    -e GITHUB_ACTIONS=true \
    -v "/var/run/docker.sock":"/var/run/docker.sock" \
    -v "/home/runner/work/_temp/_github_home":"/github/home" \
    -v "/home/runner/work/_temp/_github_workflow":"/github/workflow" \
    -v "/home/runner/work/KSPAddonVersionChecker/KSPAddonVersionChecker":"/github/workspace" af96b4:55d270f4dba34dbc989049259055c0ad  "arg1" "arg2"
```


## Based on instructions to create a Docker GitHub Action found here:

> To get started, click the `Use this template` button on this repository [which will create a new repository based on this template](https://github.blog/2019-06-06-generate-new-repositories-with-repository-templates/).
>
> For info on how to build your first Container action, see the [toolkit docs folder](https://github.com/actions/toolkit/blob/master/docs/container-action.md).
>
> https://help.github.com/en/actions/automating-your-workflow-with-github-actions/building-actions
