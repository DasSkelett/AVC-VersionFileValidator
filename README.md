# KSP-AVC Version File Validator

## Usage
```yaml
name: Validate AVC .version files
on: [push]
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

Based on instructions to create a Docker GitHub Action found here:

> To get started, click the `Use this template` button on this repository [which will create a new repository based on this template](https://github.blog/2019-06-06-generate-new-repositories-with-repository-templates/).
> For info on how to build your first Container action, see the [toolkit docs folder](https://github.com/actions/toolkit/blob/master/docs/container-action.md).
> https://help.github.com/en/actions/automating-your-workflow-with-github-actions/building-actions