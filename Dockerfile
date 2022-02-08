FROM python:3.10-alpine as base

COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
COPY validator/ /validator/
COPY main.py /main.py
CMD ["/main.py"]
