FROM python:3.13

EXPOSE 8001

RUN python3.13 -m pip install fastapi[standard]
RUN python3.13 -m pip install uvicorn
RUN python3.13 -m pip install httpx
RUN python3.13 -m pip install psycopg2
RUN python3.13 -m pip install sqlalchemy
RUN python3.13 -m pip install sqlalchemy-utils

ADD libs /UsersService/libs
ADD models /UsersService/models
ADD main.py /UsersService/

WORKDIR /UsersService/