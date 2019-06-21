FROM python:3.7

ENV PYTHONBUFFERED 1
RUN mkdir -p /project/src/itechart_project
WORKDIR /project/src/itechart_project

COPY api_app itechart_project main_app static .env manage.py requirements.txt /project/src/itechart_project/
RUN pip install -r requirements.txt
