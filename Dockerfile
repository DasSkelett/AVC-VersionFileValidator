FROM python:3.8-alpine

ENV GITHUB_WORKSPACE $GITHUB_WORKSPACE
COPY $GITHUB_WORKSPACE $GITHUB_WORKSPACE

COPY LICENSE README.md /

COPY entrypoint.sh /entrypoint.sh
COPY validator/main.py /main.py

RUN pip install jsonschema requests

ENTRYPOINT ["/entrypoint.sh"]
