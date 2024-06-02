FROM python:3.11-bookworm

WORKDIR /app

RUN python3 -m pip install --upgrade pip

COPY requirements.txt requirements_dev.txt ./

RUN pip install -r requirements.txt &&

COPY . .

RUN pip install .

RUN mkdir ./gpu4bdgamers/logs

ENV PROJECT_ROOT=/app/gpu4bdgamers

CMD [ "python3", "./gpu4bdgamers/main.py" ]
