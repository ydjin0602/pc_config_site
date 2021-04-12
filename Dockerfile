FROM python:3.8-alpine

ENV  PYTHONUNBUFFERED 1

WORKDIR /src/

RUN apk update && \
    apk --no-cache add  \
            postgresql-dev \
            python3-dev \
            gcc \
            musl-dev \
            libffi-dev && \
    rm -rf /var/cache/apk/*

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip && \
     pip install gunicorn uvicorn && \
     pip install psycopg2 && \
     pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]

CMD python manage.py runserver 0.0.0.0:8000