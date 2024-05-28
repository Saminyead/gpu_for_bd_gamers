FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN apk add --no-cache \
    build-base \
    openblas-dev \
    gfortran \
    python3-dev \
    musl-dev \
    freetype-dev \
    libpng-dev

RUN python3 -m pip install --upgrade pip

RUN pip install -r requirements.txt &&\
    pip install -r requirements_dev.txt

RUN pip install .

RUN mkdir ./gpu4bdgamers/logs

RUN mkdir ./tests/integration_test/logs

RUN cd ./gpu4bdgamers

CMD [ "python3", "main.py" ]