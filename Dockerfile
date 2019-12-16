FROM python:3.8-alpine as base

COPY validator/ /validator/

RUN pip install jsonschema requests

ENTRYPOINT ["python3.8"]


FROM base as dev
COPY tests/ /tests/
CMD ["./validator/main.py"]


FROM base
CMD ["/validator/main.py"]
