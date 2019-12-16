FROM python:3.8-alpine as base

COPY entrypoint.sh /entrypoint.sh
COPY validator/ /validator/

RUN pip install jsonschema requests

WORKDIR /

ENTRYPOINT ["/entrypoint.sh"]


FROM base as dev
COPY tests/ /tests/


FROM base
