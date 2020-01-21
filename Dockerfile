FROM python:3.8-alpine as base
COPY validator/ /validator/
COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
ENTRYPOINT ["python3.8"]


FROM base as tests
COPY tests/ /tests/
WORKDIR /
CMD ["-m", "unittest", "tests"]


FROM base as prod
CMD ["/validator"]
