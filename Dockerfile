FROM python:3.11-bookworm

WORKDIR /app

RUN python3 -m pip install --upgrade pip

COPY requirements.txt requirements_dev.txt ./

RUN pip install -r requirements.txt &&\
    pip install -r requirements_dev.txt

COPY crontab /etc/crontabs/root

COPY . .

RUN pip install .

RUN mkdir ./gpu4bdgamers/logs

RUN mkdir ./tests/integration_test/logs

ENV PROJECT_ROOT=/app/gpu4bdgamers

RUN pytest

CMD [ "crond", "-f" ]
