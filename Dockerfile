FROM python:3.11-alpine

WORKDIR /app

RUN apk add build-base\
    openblas-dev \
    gfortran \
    python3-dev \
    musl-dev \
    freetype-dev \
    libpng-dev

RUN python3 -m pip install --upgrade pip

COPY requirements.txt requirements_dev.txt ./

RUN pip install -r requirements.txt &&\
    pip install -r requirements_dev.txt

COPY . .

RUN pip install .

# RUN mkdir ./gpu4bdgamers/logs

# RUN mkdir ./tests/integration_test/logs

ENV PROJECT_ROOT=/app/gpu4bdgamers

WORKDIR /app/gpu4bdgamers

CMD [ "python3", "main.py" ]