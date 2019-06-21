FROM python:3.7

ENV PYTHONBUFFERED 1
RUN mkdir -p /home/itechart_project
WORKDIR /home/itechart_project

COPY . /home/itechart_project/
RUN pip install -r requirements.txt
