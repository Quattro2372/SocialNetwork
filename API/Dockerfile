FROM python:3.13

EXPOSE 8000

RUN python3.13 -m pip install fastapi[standard]
RUN python3.13 -m pip install uvicorn
RUN python3.13 -m pip install httpx

ADD libs /API/libs
ADD main.py /API/

WORKDIR /API/